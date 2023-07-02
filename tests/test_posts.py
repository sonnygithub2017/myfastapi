from app import sql_alchemy_models_user as models

def test_create_post(client, test_user):
  # 1) test_user get call will have a user account create in user table
  # 2) login the user, get token
  res = client.post("/login", json={"email":test_user["email"],
                                    "password": test_user["password"]})
  assert res.status_code == 200
  # 3) create post with token from login
  token = res.json()['access_token']
  client.headers = {
    **client.headers,
    "Authorization": f"Bearer {token}"
  }
  res = client.post("/posts", json={"title": "test-title1",
                                    "content": "test-content1"})
  print(f"create post: {res.json()}")
  assert res.status_code == 201

def test_create_post_fixture(authorized_client, client):
  res = authorized_client.post("/posts", json={"title": "test-title1",
                                    "content": "test-content1"})
  print(f"create post: {res.json()}")
  assert res.status_code == 201
  assert res.json()['title'] == "test-title1"

  res = client.get("/posts/")
  print(f"get post: {res.json()}")
  assert res.status_code == 200

# the user not have account in user table, no test_user
def test_unauthorized_user_no_acct_create_post(client):
  # verify we don't have user in users table
  user_res = client.get("/users")
  assert user_res.json() == []
  res = client.post("/posts", json={"title": "test-title1",
                                    "content": "test-content1"})
  print(f"create post: {res.json()}")
  assert res.status_code == 401

# the user have account in user table but not login, have test_user
def test_unauthorized_user_have_acct_create_post(client, test_user):
  # verify we have user in users table
  user_res = client.get("/users")
  assert user_res.json()[0]['id'] == test_user['id']
  res = client.post("/posts", json={"title": "test-title1",
                                    "content": "test-content1"})
  print(f"create post: {res.json()}")
  assert res.status_code == 401

def test_get_all_posts(pre_create_posts, client):
  res = client.get("/posts/")
  assert res.status_code == 200
  assert len(res.json()) == len(pre_create_posts)
  print(f"get allposts: {res.json()}")
  print(f"precreate: {pre_create_posts[0].title}")
    
  for res_post in res.json():
    for pre_post in pre_create_posts:
      if res_post['Post']['id'] == pre_post.id:
        assert res_post['Post']['title'] == pre_post.title
        assert res_post['Post']['content'] == pre_post.content

  assert res.json()[0]['Post']['owner_id'] == pre_create_posts[0].owner_id

def test_get_one_post(pre_create_posts, client):
  res = client.get(f"/posts/{pre_create_posts[0].id}")
  print(f"get that posts: {res.json()}")
  assert res.status_code == 200
  res_post =  res.json()['Post']
  assert res_post['id'] == pre_create_posts[0].id
  assert res_post['title'] == pre_create_posts[0].title

def test_get_post_not_exist(pre_create_posts, client):
  not_exist_post_id = 8888
  res = client.get(f"/posts/{not_exist_post_id}")
  print(f"get that posts: {res.json()}")
  assert res.status_code == 404

def test_authorized_user_delete_post(authorized_client, test_user, pre_create_posts):
  # verify we have user in users table
  user_res = authorized_client.get("/users")
  assert user_res.json()[0]['id'] == test_user['id']
  res = authorized_client.delete(f"/posts/{pre_create_posts[0].id}")
  assert res.status_code == 204

# the user have account in user table but not login
# note: pre_create_posts are created with test_user
def test_unauthorized_user_have_acct_delete_post(client, test_user, pre_create_posts):
  # verify we have user in users table
  user_res = client.get("/users")
  assert user_res.json()[0]['id'] == test_user['id']
  res = client.delete(f"/posts/{pre_create_posts[0].id}")
  print(f"delete post: {res.json()}")
  assert res.status_code == 401

def test_delete_non_existing_post(authorized_client, pre_create_posts):
  not_exist_post_id = 8888
  res = authorized_client.delete(f"/posts/{not_exist_post_id}")
  assert res.status_code == 404

# here pre_create_posts have posts posted by test_user (authorized_client)
# and test_user2
def test_delete_other_user_post(authorized_client, test_user, pre_create_posts):
  # get the post not posted by test_user
  other_user_post_id = None
  for post in pre_create_posts:
    if post.owner_id != test_user['id']:
      other_user_post_id = post.id
      break
  res = authorized_client.delete(f"/posts/{other_user_post_id}")
  assert res.status_code == 403

def test_authorized_user_update_post(authorized_client, pre_create_posts):
  update_data = {'title': 'updated title', 'content': 'updated content'}
  res = authorized_client.put(f"/posts/{pre_create_posts[0].id}", json=update_data)
  assert res.status_code == 200
  assert res.json()['title'] == update_data['title']

def test_update_other_user_post(authorized_client, test_user, pre_create_posts):
  update_data = {'title': 'updated title', 'content': 'updated content'}
  other_user_post_id = None
  for post in pre_create_posts:
    if post.owner_id != test_user['id']:
      other_user_post_id = post.id
      break
  res = authorized_client.put(f"/posts/{other_user_post_id}", json=update_data)
  assert res.status_code == 403

def test_unauthorized_user_update_post(client, pre_create_posts):
  update_data = {'title': 'updated title', 'content': 'updated content'}
  res = client.put(f"/posts/{pre_create_posts[0].id}", json=update_data)
  print(f"update res: {res.json()}")
  assert res.status_code == 401

def test_delete_non_existing_post(authorized_client, pre_create_posts):
  not_exist_post_id = 8888
  update_data = {'title': 'updated title', 'content': 'updated content'}
  res = authorized_client.put(f"/posts/{not_exist_post_id}", json=update_data)
  assert res.status_code == 404