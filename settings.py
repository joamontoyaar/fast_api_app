import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL= os.get( "REDIS_URL", "redis://localhost:6379" )
QUEUES= [ "emails", "default" ]

# rq worker -c settings           # Run the 'rq worker'