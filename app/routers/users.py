from .. import schemas,utils,models
from fastapi import Body, FastAPI , Response, status , HTTPException , Depends , APIRouter
from ..database import get_db
from sqlalchemy.orm import session # to create session 


router = APIRouter(
    prefix= "/users",
    tags=["users"]
)

@router.post("/create",status_code=status.HTTP_201_CREATED,response_model=schemas.user_response)
def create_user(user:schemas.users, db: session = Depends(get_db)):
    hashed_pass = utils.hash(user.password)
     # hashing the password
    user.password = hashed_pass
    new_user = models.user(**user.dict()) 
    db.add(new_user)  
    db.commit() 
    db.refresh(new_user)  
    return  new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.user_response)
def get_user(id:int,db : session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} does not exist")
    return user

