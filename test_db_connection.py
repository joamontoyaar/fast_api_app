import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

engine = create_engine( os.getenv( "DATABASE_URL" ) )

def test_db_connection():
        
    try:
        connection = engine.connect()
        print( "Connection successful!" )
    except Exception as e:
        print( f"Connection failed: {e}" )