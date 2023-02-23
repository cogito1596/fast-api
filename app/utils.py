from passlib.context import CryptContext # to hash the passwords

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # setting the schema to be used 

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_pass,hass_pass):
    return pwd_context.verify(plain_pass,hass_pass)
