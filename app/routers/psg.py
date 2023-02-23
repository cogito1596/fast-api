from fastapi import Body, FastAPI , Response, status , HTTPException , Depends , APIRouter
import psycopg2 # driver for postgres connection 
from psycopg2.extras import RealDictCursor # to get all the coloum name included  
import time
from typing import  List
from .. import schemas


router = APIRouter(
    tags=["psg_posts"]
)


while True:
    # The code will not execute untill the connection is made 
    try:
        conn = psycopg2.connect(host="localhost",database = "fast api", user = "postgres", password = "Onelove@1975" , cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection is succesful")
        break
    except Exception as error:
        print ("Connection to database is Failed")
        print("Error:", error)
        time.sleep(20)




@router.get("/",response_model=List[schemas.post]) # decorator with the method 
async def Get_all_Messages():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.response)
async def create_posts(new_post:schemas.post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.content, new_post.published))
    Data_post = cursor.fetchone()
    # we can only store in variable after you fetchone or fetchall from cursor object
    conn.commit()
    return Data_post

@router.get("/get/{id}",response_model=schemas.response)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """ ,(id,))
    # %s should always be iterable we are making id(int) iterable by keeping "," as it makes a tuple which is iterable 
    single_post = cursor.fetchone()  
    if not single_post:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Post with id: {id} is not found in our database")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"Post with id: {id} is not found in our database"}
    return  single_post

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_single_post(id:int):
    cursor.execute("""DELETE  FROM posts where id = %s RETURNING *""",(id,))
    Deleted_post = cursor.fetchone()
    conn.commit()
    if Deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"No posts available with id: {id}")
    # Note: Delete never gives you output its always 204 No content 
    return status.HTTP_204_NO_CONTENT

@router.put("/update/{id}",response_model=schemas.response)
def update_post(id:int, post:schemas.post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    # The change occurs only when you commit the changes
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"No posts available with id: {id}")
    return updated_post