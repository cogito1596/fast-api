from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from typing import Optional

class post(BaseModel):
    #pydantic model which is used for schema validation of receiving inouts
    title:str
    content:str
    published: bool = True # defaulting the value
    class Config:
        orm_mode = True

class user_response(BaseModel):
    email:EmailStr
    created_at: datetime
    id:int
    
    class Config:
        orm_mode = True

class response(post): # inhereting post
    # every model should extend base model
    id:int
    created_at: datetime
    user_id: int
    owner : user_response
    """we use class config becuase pydantic only deals with dictionary not orm 
    objects (Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict) """
    # here we are setting the config value that is y we use "=" 
    # we use ":" for declaring the type


class post_likes(BaseModel):
    Post:response
    votes:int

    class Config:
        orm_mode = True



class users(BaseModel):
    email:EmailStr
    password:str



class user_login(BaseModel):
    email:EmailStr
    password:str
    
class token_data(BaseModel):
    id:Optional[str]
    
class vote(BaseModel):
    dir:conint(le=1)
    post_id:int