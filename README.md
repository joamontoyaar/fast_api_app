# flask run

.flaskenv
FLASK_APP=app
FLASK_ENV=development

FLASK_DEBUG=1           # Se pone para q el servidor se resetee cada vez q guardo cambios en 'app.py', porq con 'flask_env' no pasa


# Build the image in Docker 
docker run -dp 5000:5000 image_name

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" image_name


# Migrate database with flask
flask db migrate        # La librería 'alembic' ve lo que hay en la DB existente y la definida por los 'models', y crea un script para migrar desde estos hacia la DB. Si no hay DB, crea una en blanco basada en los 'models'

flask db upgrade        # Crea todas las tablas en la base de datos según los esquemas y demás info, desde la versión actual hacia la última versión (definida en 'models')
