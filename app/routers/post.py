from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import sql_alchemy_models_user as models, \
  pydantic_schema_user as schema, oauth2
from ..sql_alchemy_db import get_db

router = APIRouter(
   prefix="/posts",
   tags=["Posts"]
)

# list[schema.ResponsePost] convert to list 
@router.get("/", response_model=list[schema.ResponsePostVote])
#@router.get("/")
def get_posts(db: Session=Depends(get_db),
              limit:int=10, skip:int=0, search:str=""):
  # cur.execute("SELECT * FROM posts")
  # my_posts = cur.fetchall() 
  
  # without join
  # my_posts = db.query(models.Post).filter(models.Post.title.contains(search))\
  #   .limit(limit).offset(skip).all()

  # with join
  # sql: SELECT posts.*, COUNT(votes.post_id) as num_votes FROM posts 
  #   LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;
  # results = (
  #   db.query(models.Post, func.count(models.Vote.post_id).label("num_votes"))
  #   .join(models.Vote, models.Vote.post_id == models.Post.id,
  #   isouter=True).group_by(models.Post.id).all()
  # )

  results = (
    db.query(models.Post, func.count(models.Vote.post_id).label("num_votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id,
    isouter=True).group_by(models.Post.id)
    .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    .all()
  )

  
  # serialize the results to list of dict
  # my_posts = []
  # for post, num_votes in results:
  #    post_dict = post.__dict__  # convert post obj to dict
  #    post_dict["num_votes"] = num_votes
  #    my_posts.append(post_dict)

  return results

# change status of creation as 201 instead of 200
@router.post("/", status_code=status.HTTP_201_CREATED,
          response_model=schema.ResponsePost) 
def create_posts(post: schema.CreatePost, db: Session=Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
  # save the post to db with INSERT INTO
  # cur.execute("INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * ", 
  #             (post.title, post.content, post.published))
  # new_post = cur.fetchone()
  # conn.commit()

  # new_post = models.Post(title=post.title, content=post.content,
  #                        published=post.published)
  # use unpack dicts
  print("***** current_user: *****")
  print(current_user.id)
  new_post = models.Post(owner_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post # return back
    
# use HTTPException from fastapi to handle it
#@router.get("/{id}", response_model=schema.ResponsePost)
@router.get("/{id}", response_model=schema.ResponsePostVote)  
def get_post(id: int, db: Session=Depends(get_db)):
  # cur.execute("SELECT * FROM posts WHERE id=%s", (str(id))) 
  # post = cur.fetchone()
  #post = db.query(models.Post).filter(models.Post.id == id).first()

  post = (
    db.query(models.Post, func.count(models.Vote.post_id).label("num_votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id,
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  )
  if not post:
      raise HTTPException(status.HTTP_404_NOT_FOUND,
                          f"no post with this id: {id}")
  return post

# use HTTP_204_NO_CONTENT and HTTPException from fastapi 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id: int, db: Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
  # cur.execute("DELETE FROM posts where id = %s RETURNING *", (str(id)))
  # deleted_post = cur.fetchone()
  # conn.commit()
  deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
  if not deleted_post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"no post with this id: {id}")
  if deleted_post.owner_id != current_user.id:
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail="User not allowed to delete the post")
  db.delete(deleted_post)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

# update(put)
@router.put("/{id}", response_model=schema.ResponsePost) 
def update_post(id: int, post: schema.CreatePost,
                db: Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
  # cur.execute("""UPDATE posts SET title = %s, content = %s 
  #             WHERE id = %s RETURNING * """, 
  #             (post.title, post.content, str(id)))
  # updated_post = cur.fetchone()
  # conn.commit()

  updated_post = db.query(models.Post).filter(models.Post.id == id)
  if not updated_post.first():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"no post with this id: {id}")
  if updated_post.first().owner_id != current_user.id:
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail="User not allowed to update the post")
  updated_post.update(post.dict()) 
  # here post.dict() is user input updated post in dict
  db.commit()
  return updated_post.first()