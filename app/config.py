from pydantic import BaseSettings

class MySettings(BaseSettings):
  database_username: str
  database_password: str
  database_hostname: str
  database_port: str
  database_name: str
  secret_key: str
  algorithm: str
  access_token_expire_mimutes: int

  class Config:
    env_file = ".env"

settings = MySettings()