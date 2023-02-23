from .database import Base
from sqlalchemy import Column, INTEGER , String, Boolean , ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    # every class extends base class 
    __tablename__ = "alchmey_posts"

    id = Column(INTEGER, primary_key = True,nullable = False)
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default="True",nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

    user_id = Column(INTEGER,ForeignKey("users.id", ondelete = "CASCADE"),nullable=False)
    owner = Relationship("user")

    """ if you make changes to class without changing name they will not effected as sql alchemy 
    only checks if the class name existed  """
    
class user(Base):
    __tablename__ = "users"

    id = Column(INTEGER,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

class likes(Base):
    __tablename__ = "votes"
    # use of composite keys to keep both together unique
    post_id =  Column(INTEGER,ForeignKey("alchmey_posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(INTEGER,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

