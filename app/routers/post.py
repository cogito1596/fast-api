from .. import schemas,models,oauth2
from fastapi import Body, FastAPI , Response, status , HTTPException , Depends , APIRouter
from ..database import get_db
from sqlalchemy.orm import session # to start a session
from sqlalchemy import func
from typing import   List , Optional

router = APIRouter(
    tags=["Alchmey_posts"]
)

# ,response_model=list[schemas.post_likes]
@router.get("/alchemy/get",response_model=list[schemas.post_likes])
def alchemy_get(db: session = Depends(get_db),limit:int = 10,skip:int = 0,search:Optional[str] = "") :
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # we need to pass db in every argument for session to get created it will call get_db function 
    posts = db.query(models.Post, func.count(models.likes.post_id).label("votes")).join(models.likes,models.likes.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router.post("/palchemy/post",response_model=schemas.response,status_code=status.HTTP_201_CREATED)
def alchemy_post(post:schemas.post, db: session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = get_current_user.id,**post.dict()) # we are unpacking dictionary 
     
    db.add(new_post) # we need to use add to put in staging area 
    db.commit() # we need to commmit to update the changes in db
    db.refresh(new_post) # we are updating the new_post with the output of the query (its like returning in driver)
    return  new_post

@router.get("/galchemy/{id}",response_model=schemas.post_likes)
def alchemy_id(id:int, db:session = Depends(get_db)):
    single_id = db.query(models.Post, func.count(models.likes.post_id).label("votes")).join(models.likes,models.likes.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if single_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not post available with id : {id}")

    # use filter for where condition
    #using first stops process afte we get one result
    return single_id

@router.delete("/dalchemy/{id}")
def delete_id(id:int, db:session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not post available with id : {id}")
    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not allowed to perform this action")
    deleted_post.delete(synchronize_session =False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/palchemy/{id}",response_model=schemas.response)
def update_id(id:int,updated_post:schemas.post, db:session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    updated_query = db.query(models.Post).filter(models.Post.id ==id) # This basically constructs sql query
    post_available = updated_query.first()
    if post_available == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not post available with id : {id}")
    if post_available.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not allowed to perform this action")
    updated_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return updated_query.first()