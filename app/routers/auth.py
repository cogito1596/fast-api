from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # safe way to get password 
from sqlalchemy.orm import Session
from ..import database , schemas , models , utils , oauth2
router = APIRouter()

# Depends is generally used to inject parameters into endpoint 
@router.post("/login")
def login(user_cred:OAuth2PasswordRequestForm = Depends()  ,db:Session = Depends(database.get_db)): # we use orm objects only for query 
    user = db.query(models.user).filter(models.user.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"user with email id:{user_cred.username} does not exist")

    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="The invalid credentials")
    
    access_token = oauth2.create_token({"user_id":user.id})

    return {"accesss_token":access_token, "token_type":"bearer"}
    