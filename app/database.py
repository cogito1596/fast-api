from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_URL = f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'%quote_plus(settings.database_password)

# SQLALCHEMY_URL = '<databaseName>://<username>:<password>/@ip/<databaseName inside database>'

def get_db():
    # This is the function that is called to create a session and close it when finished
    db = SessionLocal() # every instance of class session local is a actual database session
    try:
        yield db
    finally:
        db.close()

engine = create_engine(SQLALCHEMY_URL) #This is to create engine for respective database
SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)
Base = declarative_base() # we will inherit these class to make models and classes

