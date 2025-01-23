# flask run

.flaskenv
FLASK_APP=app
FLASK_ENV=development

FLASK_DEBUG=1           # Se pone para q el servidor se resetee cada vez q guardo cambios en 'app.py', porq con 'flask_env' no pasa


# Build the Docker image with the Dockerfile

docker build -t image_name .    


# Docker compose: Build the imaage, start the container, and show logs
docker compose up


# Run the image in Docker locally. A container is generated with the specified image
docker run -dp 5000:5000 image_name

docker run -dp 5000:5000 -w /app -v ".:/app" image_name

docker run -dp 5000:5000 -w /app -v ".:/app" image_name sh -c "flask run --host 0.0.0.0          
#    Este comando le dice al Docker que NO corra el 'CMD' del Dockerfile, sino que ejecute "flask run"


# Migrate database with flask
flask db migrate        # La librería 'alembic' ve lo que hay en la DB existente y la definida por los 'models', y crea un script para migrar desde estos hacia la DB. Si no hay DB, crea una en blanco basada en los 'models'

flask db upgrade        # Crea todas las tablas en la base de datos según los esquemas y demás info, desde la versión actual hacia la última versión (definida en 'models')



# Run the app in Docker
CMD ["flask", "run", "--host", "0.0.0.0"]           # To run with flask

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]


# Re-create the db image
docker compose up --build --force-recreate --no-deps db


# Database connection string
postgresql://db_user:db_password@db_host:5432/db_name         # 5432 es el puerto de la máquina local.   db_host= localhost cuando es on premise

DATABASE_URL=postgresql://postgres:password@db:5432/myapp 


# 'Docker-entrypoint.sh' es un script que va a correrse antes de correr el Dockerfile
#   Este comando le dice a container que corra el 'docker-entrypoint'. NO es la imagen a construir
#   La idea es que el contenedor siempre ejecute 'docker-entrypoint' antes de empezar, osea que primero corre las migraciones de la base de datos antes de iniciar la ejecución del servicio (la API). Si no hay migraciones pendientes, simplemente la omite y corre el servicio.
CMD ["/bin/bash", "docker-entrypoint.sh"]      