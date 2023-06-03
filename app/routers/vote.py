from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import sql_alchemy_models_user as models, \
  pydantic_schema_user as schema, oauth2
from ..sql_alchemy_db import get_db

router = APIRouter(
   prefix="/votes",
   tags=["Votes"]
)

# change status of creation as 201 instead of 200
@router.post("/", status_code=status.HTTP_201_CREATED) 
def post_vote(vote: schema.Vote, db: Session=Depends(get_db),
              current_user=Depends(oauth2.get_current_user)):
  found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not found_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {vote.post_id} is not exist")
  
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                          models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()
  if vote.vote_dir: # vote the post
    if found_vote:  # already voted
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, \
        detail=f"post {vote.post_id} already voted by user: {current_user.id}")
    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return {"msg": f"Successfully vote post {vote.post_id} by user: {current_user.id}"}
  else:  # remove the vote
    if not found_vote:  # have not voted
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
        detail=f"post {vote.post_id} NOT voted by user: {current_user.id}")
    db.delete(found_vote)
    db.commit()
    return {"msg": f"Successfully delete vote for post {vote.post_id} by user: {current_user.id}"}
  