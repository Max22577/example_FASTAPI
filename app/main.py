import time
from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import posts, users, auth, votes


models.Base.metadata.create_all(bind = engine)


app = FastAPI()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}



while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'newfastAPI', user = 'postgres', password = 'vanessa#2400', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)
        time.sleep(3)
   
        
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/sqlalchemy", response_model=schemas.Post)
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    
    
@app.get("/")
def root():
    return {"message": "Welcome to my API"}


