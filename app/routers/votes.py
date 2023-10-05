from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter
from .. import database, schemas, models, Oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(Oauth2.get_current_user)):
    post = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id was not found')
    vote_query = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'current user has already voted')
        new_vote = models.Vote(posts_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Successfully deleted post'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exsist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {'message': 'Successfully deleted post'}