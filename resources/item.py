from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel


blp= Blueprint( "items", "items", description= "Operations on items" )


@blp.route( "/item/<int:item_id>" )
class Item( MethodView ):

  @jwt_required()
  @blp.response( 200, ItemSchema )                      # Este decorador está "formateando" la respuesta con base en el 'ItemSchema' definido, por lo que la respuesta al cliente va a contener dichos campos
  def get( self, item_id ):
    try:
      item= ItemModel.query.get_or_404( item_id )
      return item
    except KeyError:
      abort( 404, message= "Item not found" )

  

  @jwt_required()
  def delete( self, item_id):
    try:

      jwt= get_jwt()

      if not jwt.get( "is_admin" ):
        abort( 401, message= "Admin privilege required." )
      
      
      item= ItemModel.query.get_or_404( item_id )
      db.session.delete( item )
      db.session.commit()

      return { "message": "Item deleted" }
    except KeyError:
      abort( 404, message= "Item not found" )



  @blp.arguments( ItemUpdateSchema )
  @blp.response( 200, ItemSchema )
  def put( self, item_data, item_id ):                  # Ya no es necesario poner explícita (capturar) la info del 'request' y asignarla a una variable, el decorador lo hace y lo pasa como argumentos, incluso los asinga primero (item_data) al frente de los argumentos raíz (root arguments), que en este case es 'item_id'
    # item_data= request.get_json()      
    try:
      item= ItemModel.query.get( item_id )

      if item:
        item.price= item_data[ "price" ]
        item.name= item_data[ "name" ]
      else:
        item= ItemModel( id= item_id, **item_data )

      db.session.add( item )
      db.session.commit()
      return item
    
    except KeyError:
      abort( 404, message= "Item not found" )




@blp.route( "/item")
class ItemList( MethodView ):

  @jwt_required()
  @blp.response( 200, ItemSchema( many= True ) )        # 'many= True' convierte la respuesta en una lista de items
  def get( self ):
    # return { "items": list( items.values() ) }        # Antes devolvía un objeto con una lista de objetos
    return ItemModel.query.all()
  

  @jwt_required( fresh= True )
  @blp.arguments( ItemSchema )                          # Este decorador sirve como intermediario para la info del JSON que el cliente envía, validando que los datos no solo vengan en el 'request', sino el tipo de dato tal y como se especificó en el 'ItemSchema' del "schema.py". Luego es posible asignarlo como un argumento en la función. De esta manera, ya no es necesario hacer una validación manual de los datos, por ejemplo " if 'name' in item_data"
  @blp.response( 201, ItemSchema )
  def post( self, item_data ):                          # El segundo argumento (en este caso 'items_data') va a contener el JSON con los campos validados que 'Schema' solicitó. 
    # item_data= request.get_json()                     # Ya no es necesario poner explícita (capturar) la info del 'request' y asignarla a una variable, el decorador lo hace y lo pasa como argumentos, incluso los asinga al frente de e los argumentos raíz (root arguments)

    item= ItemModel( **item_data )                      # '**item_data' coge el diccionario q captura del 'request' y lo convierte en 'keyword arguments' y lo carga en 'ItemModel'

    try:
      db.session.add( item )
      db.session.commit()
    except SQLAlchemyError:
      abort( 500, message= "An error occurred while inserting the item." )

    return item, 201