from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passwd: str):  
  return pwd_context.hash(passwd)

def verify_password(plain_passwd, hashed_passwd):
  return pwd_context.verify(plain_passwd, hashed_passwd)