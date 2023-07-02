from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import sql_alchemy_db as database, pydantic_schema_user as schemas, \
  sql_alchemy_models_user as models, utils, oauth2

router = APIRouter(tags=["Authentication"])
@router.post('/login')
def login(user_credentials: schemas.UserLogin,
          db: Session=Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.email == 
                  user_credentials.email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"User not created")  
  if not utils.verify_password(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Invalid Credentials")
  # create token
  access_token = oauth2.create_access_token(data={"user_id": user.id})
  return {"access_token": access_token, "token_type": "bearer"}
