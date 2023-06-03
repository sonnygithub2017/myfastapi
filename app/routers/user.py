from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import sql_alchemy_models_user as models, \
  pydantic_schema_user as schema, utils
from ..sql_alchemy_db import get_db

router = APIRouter(
   prefix="/users",
   tags=["Users"]
)
@router.post("/", status_code=status.HTTP_201_CREATED,
          response_model=schema.OutUser) 
def create_user(user: schema.InUser, db: Session=Depends(get_db)):
  user.password = utils.hash(user.password)
  new_user = models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user # return back

@router.get("/", response_model=list[schema.OutUser])
def get_users(db: Session=Depends(get_db)): 
  my_users = db.query(models.User).all()
  return my_users

@router.get("/{id}", response_model=schema.OutUser)  
def get_user(id: int, db: Session=Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
      raise HTTPException(status.HTTP_404_NOT_FOUND,
                          f"no user with this id: {id}")
  return user