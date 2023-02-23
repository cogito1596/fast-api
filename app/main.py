from . import models , schemas , utils
from .database import engine, get_db
from fastapi import Body, FastAPI , status , HTTPException , Depends
from sqlalchemy.orm import session # to create session 
from .routers import post,users,psg,auth,votes
from fastapi.middleware.cors import CORSMiddleware

# go to url and /docs provides documentation

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(post.router)
app.include_router(users.router)
app.include_router(psg.router)
app.include_router(auth.router)
app.include_router(votes.router)
# use include router to check the paths
        

models.Base.metadata.create_all(bind=engine) # This will start the orm engine 



 




