from models.store import StoreModel
from models.item import ItemModel
from models.tag import TagModel
from models.item_tags import ItemTags
from models.user import UserModel


# Esto ayuda a la importación de los modelos en las otras carpetas, en el sentido que '__init__.py' va a 
#  realizar la importación (como un intermediario para los demás módulos que necesiten importar los modelos y
#   no es necesario expresar el comando completo sino simplemente poner:
# 
#   from models import StoreModel