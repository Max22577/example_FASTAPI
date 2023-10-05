from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, Oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status, APIRouter


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 7, search: Optional[str] = ''):
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    posts = db.query(models.Post, func.count(models.Vote.posts_id).label("votes")).join(models.Vote, models.Vote.posts_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    print(posts)
    return posts

@router.post("/createposts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(body: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    #new_post = models.Post(title= body.title, content = body.content, published = body.published)
    print(current_user.email)
    new_body = body.dict()
    new_body['owner_id'] = current_user.id
    new_post = models.Post(**new_body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""",(body.title, body.content, body.published))
    #new_post = cursor.fetchone()  
    #conn.commit() 
    return new_post


@router.get("/{id}", response_model= schemas.Post)
def get_one_post(id: int,  db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
 
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with {id} not found')
       #response.status_code = status.HTTP_404_NOT_FOUND
       #return {'detail': f'post with {id} not found'}
    print(post)
    return post

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #index = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id {id} was not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Not authorized to perform this task')
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    #index = cursor.fetchone()
    #conn.commit()
    new_post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = new_post_query.first()
    if new_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id {id} was not found')
    
    if new_post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Not authorized to perform this task')
   
    new_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    pst = new_post_query.first()
   
    return pst
