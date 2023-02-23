from pydantic import BaseSettings

class setting(BaseSettings):
    database_hostname:str
    database_password:str
    database_name:str = "postgres"
    database_port:str
    database_username:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30

    class Config:
        env_file = ".env"

settings = setting()