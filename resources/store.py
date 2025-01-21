from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import StoreSchema
from models import StoreModel


blp= Blueprint( "stores", __name__, description= "Operations on stores" )


@blp.route( "/store/<int:store_id>" )
class Store( MethodView ):

  @blp.response( 200, StoreSchema )                           
  def get( self, store_id ):
    try:      
      store= StoreModel.query.get_or_404( store_id )
      return store
    except KeyError:
      raise NotImplementedError( "Deleting a store is not implemented." )
      # abort( 404, message= "Store not found" )

  
  def delete( self, store_id):
    try:
      store= StoreModel.query.get_or_404( store_id )
      db.session.delete( store )
      db.session.commit()

      return { "message": "Store deleted" }
    except KeyError:
      abort( 404, message= "Store not found" )



@blp.route( "/store")
class StoreList( MethodView ):

  @blp.response( 200, StoreSchema( many= True ) )
  def get( self ):
    # return { "stores": list( stores.values() ) }
    return StoreModel.query.all()
  

  @blp.arguments( StoreSchema )
  @blp.response( 201, StoreSchema )
  def post( self, store_data ):
    # store_data= request.get_json()
    
    store= StoreModel( **store_data )

    try:
      db.session.add( store )
      db.session.commit()
    except IntegrityError:
      abort( 400, message= "A store with that name already exists." )
    except SQLAlchemyError:
      abort( 500, message= "An error occurred creating the store." )

    return store, 201