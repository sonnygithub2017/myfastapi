from datetime import datetime
from pydantic import BaseModel, EmailStr

# define the schema class with pydantic
class InUser(BaseModel):
  email: EmailStr
  password: str

class OutUser(BaseModel):
  id: int
  email: EmailStr
  class Config:
    orm_mode = True

class BasePost(BaseModel):
  title: str        # required
  content: str      # required
  published: bool = True   # with default

class CreatePost(BasePost):
  pass

class ResponsePost(BasePost):
  id: int
  title: str
  create_at: datetime
  owner_id: int
  owner: OutUser

  # following will convert ORM object into pydantic dict
  class Config:
    orm_mode = True

class ResponsePostVote(BaseModel):
  Post: ResponsePost
  num_votes: int
  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class TokenData(BaseModel):
  id: int

class Vote(BaseModel):
  post_id: int
  vote_dir: bool