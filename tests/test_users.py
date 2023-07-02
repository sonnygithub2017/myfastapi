import pytest
from jose import jwt
from app import pydantic_schema_user as schema
#from .database import client, session
from app.config import settings

def test_root(client):
  res = client.get("/")
  assert res.status_code == 200, "root get should return 200 as status_code"
  assert res.json() == {"message": "Hello World"}
  print(f"json: {res.json()}")
  print(f"text: {res.text}")

def test_create_user(client):
  res = client.post("/users/", json={"email":"test-user@gmail.com",
                                    "password": "testpass123"})
  assert res.status_code == 201
  #assert res.json().get("email") == "test-user@gmail.com"
  res_user = schema.OutUser(**res.json())
  assert res_user.email == "test-user@gmail.com"
  print(f"test_user: {res_user.email}")

def test_login(client, test_user):
  res = client.post("/login", json={"email":test_user["email"],
                                    "password": test_user["password"]})
  assert res.status_code == 200
  res_dict = res.json()
  print(f"test_login: {res_dict}")  # have access_token and token_type
  payload = jwt.decode(res_dict["access_token"], settings.secret_key,
                       algorithms=[settings.algorithm])
  assert res_dict["token_type"] == "bearer"
  assert payload.get("user_id") == test_user["id"]

def test_failed_login(client, test_user):
  res = client.post("/login", json={"email":test_user["email"],
                                    "password": "wrongpass"})
  print(f"failedlogin: {res.json()}")
  assert res.status_code == 403
  assert res.json().get("detail") == "Invalid Credentials"
 
@pytest.mark.parametrize("email, passwd, status_code", \
  [
   ("test-user@gmail.com", "wrongpass", 403),
   ("wrongemail@gmail.com", "testpass123", 401),
   ("wrongemail@gmail.com", "wrontpass", 401),
   (None, "testpass123", 422),
   ("test-user@gmail.com", None, 422)
  ])
def test_failed_login_para(client, test_user, email, passwd, status_code):
  res = client.post("/login", json={"email": email,
                                    "password": passwd})
  print(f"failedlogin_para: {res.json()}")
  assert res.status_code == status_code