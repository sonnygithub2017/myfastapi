from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:\
{settings.database_password}@{settings.database_hostname}:\
  {settings.database_port}/{settings.database_name}'

# collect to DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# use session to talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create Base to be used by others
Base = declarative_base()

# define session to talk to DB, app just call it
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()