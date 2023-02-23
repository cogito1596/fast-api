from fastapi import FastAPI , Response,status,HTTPException,Depends,APIRouter
from .. import database, models , oauth2 ,schemas
from sqlalchemy.orm import session

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/",status_code= status.HTTP_201_CREATED)
def vote(vote:schemas.vote,db:session = Depends(database.get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with post.id {vote.post_id} does not exist")

    vote_query = db.query(models.likes).filter(models.likes.post_id == vote.post_id,models.likes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with user id {current_user.id} has already voted for {vote.post_id}")
        new_vote = models.likes(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added the vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist to delete")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "vote successfully deleted"}
