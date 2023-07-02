def test_vote_on_own_post(authorized_client, pre_create_posts):
  # vote itself
  res = authorized_client.post("/votes/", json={"post_id": pre_create_posts[0].id,
                                                "vote_dir": True})
  print(f"vote own post: {res.json()}")
  assert res.status_code == 201

def test_vote_on_other_post(authorized_client, test_user, pre_create_posts):
  # vote other's user's post
  other_user_post_id = None
  for post in pre_create_posts:
    if post.owner_id != test_user['id']:
      other_user_post_id = post.id
      break
  res = authorized_client.post("/votes/", json={"post_id": other_user_post_id,
                                                "vote_dir": True})
  print(f"vote another post: {res.json()}")
  assert res.status_code == 201

# pre_vote: will add an entry to vote table with: pre_create_posts[0].id, test_user['id']
def test_vote_twice(authorized_client, pre_create_posts, pre_vote):
  res = authorized_client.post("/votes/", json={"post_id": pre_create_posts[0].id,
                                                "vote_dir": True})
  print(f"vote twice: {res.json()}")
  assert res.status_code == 409

# pre_vote, this will vote first
def test_delete_vote(authorized_client, pre_create_posts, pre_vote):
  res = authorized_client.post("/votes/", json={"post_id": pre_create_posts[0].id,
                                                "vote_dir": False})
  print(f"delete vote: {res.json()}")
  assert res.status_code == 201

# no pre_vote, so no exist vote
def test_delete_non_exist_vote(authorized_client, pre_create_posts):
  res = authorized_client.post("/votes/", json={"post_id": pre_create_posts[0].id,
                                                "vote_dir": False})
  print(f"delete non-exist vote: {res.json()}")
  assert res.status_code == 404

# no exist post
def test_delete_non_exist_post(authorized_client, pre_create_posts, pre_vote):
  non_exist_post = 8888
  res = authorized_client.post("/votes/", json={"post_id": non_exist_post,
                                                "vote_dir": True})
  print(f"delete non-exist vote: {res.json()}")
  assert res.status_code == 404

# client is unauthorized user
def test_vote_unauthorized_user(client, test_user, pre_create_posts):
  res = client.post("/votes/", json={"post_id": pre_create_posts[0].id,
                                                "vote_dir": True})
  print(f"unauthorized user to vote post: {res.json()}")
  assert res.status_code == 401