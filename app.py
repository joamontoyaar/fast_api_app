import os
import secrets
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


from sqlalchemy import create_engine

engine = create_engine( os.getenv( "DATABASE_URL" ) )

try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")



def create_app( db_url= None ):
  app= Flask( __name__ )
  # load_dotenv()                                                                             # Carga el contenido de las variables de entorno que están en el '.env'

  app.config[ "PROPAGATE_EXCEPTIONS" ]= True
  app.config[ "API_TITLE" ]= "Stores REST API with Flask"
  app.config[ "API_VERSION" ]= "v1"
  app.config[ "OPENAPI_VERSION" ]= "3.0.3"
  app.config[ "OPENAPI_URL_PREFIX" ]= "/"
  app.config[ "OPENAPI_SWAGGER_UI_PATH" ]= "/swagger-ui"
  app.config[ "OPENAPI_SWAGGER_UI_URL" ]= "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config[ "SQLALCHEMY_DATABASE_URI" ]= db_url or os.getenv( "DATABASE_URL", "sqlite:///data.db" )
  app.config[ "SQLALCHEMY_TRACK_MODIFICATIONS" ]= False
  db.init_app( app )

  migrate= Migrate( app, db )

  api= Api( app )


  app.config[ "JWT_SECRET_KEY" ]= "210874303276528023713288889381365684968"               # secrets.SystemRandom().getrandbits( 128 )
  jwt= JWTManager( app )

  ## Log Out
  #   Cada q se recibe un token, esta función lo lee y verifica que el usuario no esté en la blocklist. Si está, devuelve 'True' y ejecuta la siguiente función
  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist( jwt_header, jwt_payload ):
    return jwt_payload[ "jti" ] in BLOCKLIST 
  
  #   Retorna el mensaje cuando el usuario está en la blocklist
  @jwt.revoked_token_loader
  def revoked_token_callback( jwt_header, jwt_payload ):
    return (
      jsonify(
        { 
          "description": "The token has been revoked.",
          "error": "token_revoked"
        }
      ),
      401
    )
  
  #   Este es un 'loader' para cuando esperamos un 'fresh token', pero recibimos un 'non-fresh token'
  @jwt.needs_fresh_token_loader
  def token_not_fresh_callback( jwt_header, jwt_payload ):

    return (
      jsonify(
        {
          "description": "The token is not fresh.",
          "error": "fresh_token_required"
        }
      ),
      401
    )


  ## Claims: Allows to add extra information to JWT when is created
  @jwt.additional_claims_loader 
  def add_claims_to_jwt( identity ):

    # Look in the database whether the user is an admin
    if identity == 1:
      return { "is_admin": True }
    return { "is_admin": False }

  @jwt.expired_token_loader
  def expired_token_callback( jwt_header, jwt_payload ):

    return (
      jsonify( 
        { 
          "message": "The token has expired.", 
          "error": "token_expired." 
        } 
      ),
      401
    )
  
  @jwt.invalid_token_loader
  def invalid_token_callback( error ):

    return (
      jsonify(
        {
          "message": "Signature verification failed.",
          "error": "invalid_token"
        }
      ),
      401
    )
  
  @jwt.unauthorized_loader
  def missing_token_callback( error ):

    return (
      jsonify(
        { 
          "description": "Request does not contain an access token.", 
          "error": "authorization_required." 
        } 
      ),
      401
    )

  # # SQLAlchemy crea las tablas en la base de datos 
  # with  app.app_context():
  #   db.create_all()
  

  api.register_blueprint( ItemBlueprint )
  api.register_blueprint( StoreBlueprint )
  api.register_blueprint( TagBlueprint )
  api.register_blueprint( UserBlueprint )

  return app


