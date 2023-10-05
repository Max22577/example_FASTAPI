from typing import List
from .. import models, schemas, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter

router = APIRouter(tags=['Users'])

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_user/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
 
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User with {id} not found')
       #response.status_code = status.HTTP_404_NOT_FOUND
       #return {'detail': f'post with {id} not found'}
    print(user)
    return user

@router.put("/updateUser/{id}", response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(models.User.id == id)
    if new_user.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User with id {id} was not found')
   
    new_user.update(user.dict(), synchronize_session=False)
    db.commit()
    updated_user = new_user.first()
   
    return updated_user

@router.get("/getUsers", response_model= List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
    