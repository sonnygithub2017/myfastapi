import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.sql_alchemy_db import Base, get_db
from app import sql_alchemy_models_user as models

# newDB {settings.database_name}_test
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:\
{settings.database_password}@{settings.database_hostname}:\
  {settings.database_port}/{settings.database_name}_test'

# connect to test DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create TestingSessionLocal to talk to DB
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# fixture: function to provide baseline for others
# it has different scope, default: function scope, also have module, package or session scope
@pytest.fixture()
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture()
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)

@pytest.fixture
def test_user(client):
  userdata = {"email":"test-user@gmail.com",
              "password": "testpass123"}
  res = client.post("/users/", json=userdata) # add user to DB
  assert res.status_code == 201
  #print(f"test_user: {res.json()}")  # return user just have id and email
  new_user = res.json()
  new_user['password'] = userdata['password']  # add password to it
  return new_user

@pytest.fixture
def test_user2(client):
  userdata = {"email":"test-user2@gmail.com",
              "password": "testpass234"}
  res = client.post("/users/", json=userdata) # add user to DB
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = userdata['password']  # add password to it
  return new_user

@pytest.fixture
def login_for_token(test_user, client):
  res = client.post("/login", json={"email": test_user['email'],
                                    "password": test_user['password']})
  assert res.status_code == 200
  return res.json()['access_token']

@pytest.fixture
def authorized_client(client, login_for_token):
  client.headers ={
    **client.headers,
    "Authorization": f"Bearer {login_for_token}"
  }
  return client

# make sure the posts are created not with authorized_client
@pytest.fixture
def pre_create_posts(test_user, session, test_user2):
  # res = authorized_client.post("/posts", json={"title": "test-title1",
  #                              "content": "test-content1"})
  # assert res.status_code == 201
  # res = authorized_client.post("/posts", json={"title": "test-title2",
  #                              "content": "test-content2"})
  # assert res.status_code == 201
  # res = authorized_client.post("/posts", json={"title": "test-title3",
  #                              "content": "test-content3"})
  # assert res.status_code == 201

  posts_data = [{
    "title": "first title",
    "content": "first content",
    "owner_id": test_user['id']
    }, {
    "title": "2nd title",
    "content": "2nd content",
    "owner_id": test_user['id']
    }, {
    "title": "3rd title",
    "content": "3rd content",
    "owner_id": test_user['id']
  }, {
    "title": "4th title",
    "content": "4th content",
    "owner_id": test_user2['id']
  }]
  # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
  #                  models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
  #                  models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])

  # use unpack way, unpack dict to keyword arguments
  def model_post_dict(post_dict):
    return models.Post(**post_dict)
  post_list = list(map(model_post_dict, posts_data))
  session.add_all(post_list)
  session.commit()
 
  # list of models.Post object
  return session.query(models.Post).all()

@pytest.fixture
def pre_vote(session, pre_create_posts, test_user):
  session.add(models.Vote(post_id=pre_create_posts[0].id, user_id=test_user['id']))
  session.commit()