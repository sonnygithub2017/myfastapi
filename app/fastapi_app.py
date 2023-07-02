"""
to run following, use
(venv) sonny.li@sonnylaptop api_python_sanjeeva % 
  uvicorn app.fastapi_app:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from .sql_alchemy_db import engine
#from . import sql_alchemy_models_user as models
from .routers import post, user, auth, vote

# create tables, use sqlalchemy models to create tables
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # for every domain of web-browsers
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
      

@app.get("/")
async def root():
  return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)