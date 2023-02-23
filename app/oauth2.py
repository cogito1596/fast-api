from jose import JWTError,jwt
from datetime import timedelta, datetime
from . import schemas, database , models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    enocoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return enocoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.token_data(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data.id
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token_data =  verify_token(token,credentials_exception)
    user = db.query(models.user).filter(models.user.id == token_data).first()
  
    return user
                                          


