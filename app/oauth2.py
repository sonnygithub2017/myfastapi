from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from . import pydantic_schema_user as schemas, sql_alchemy_db as database, \
  sql_alchemy_models_user as models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MIMUTES = settings.access_token_expire_mimutes

def create_access_token(data: dict):
  """ params:
        data: dict, like {"user_id": user.id}
  """
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIMUTES)
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str=Depends(oauth2_scheme),
                           db: Session=Depends(database.get_db)):
  """
  verify token when current user send api to server with token
  params:
    token: str, jwt token. the Depends will verify it follows oauth2_scheme
    db: Session, depends will get session for DB
  """
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"couldn't validate credentials",
    headers={"WWW-Authentication": "Bearer"})
  
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if not user_id:
      raise credentials_exception
    token_data = schemas.TokenData(id=user_id)
  except JWTError:
    raise credentials_exception

  user = db.query(models.User).filter(models.User.id == token_data.id).first()
  return user