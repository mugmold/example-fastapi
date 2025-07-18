from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.schemas.vote import VoteCreate, VoteResponse
from app.core.db import get_db
from app.models.user import User as user_model
from app.models.post import Post as post_model
from app.models.vote import Vote as vote_model
from app.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VoteResponse)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user)):

    post = db.query(post_model).filter(post_model.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist.")

    query = db.query(vote_model).filter(
        and_(
            vote_model.post_id == vote.post_id,
            vote_model.user_id == current_user.id
        )
    )

    found_vote = query.first()

    if found_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="A vote for this post by the current user already exists.")

    new_vote = vote_model(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()

    total_votes = db.query(vote_model).filter(
        vote_model.post_id == vote.post_id).count()

    return {
        "message": "Vote added successfully",
        "post_id": vote.post_id,
        "total_votes": total_votes
    }


@router.delete("/", status_code=status.HTTP_200_OK, response_model=VoteResponse)
def delete_vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user)):
    post = db.query(post_model).filter(post_model.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist.")

    query = db.query(vote_model).filter(
        and_(
            vote_model.post_id == vote.post_id,
            vote_model.user_id == current_user.id
        )
    )

    found_vote = query.first()

    if not found_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Vote not found. The user has not voted on this post.")

    query.delete(synchronize_session=False)
    db.commit()

    total_votes = db.query(vote_model).filter(
        vote_model.post_id == vote.post_id).count()

    return {
        "message": "Vote removed successfully",
        "post_id": vote.post_id,
        "total_votes": total_votes
    }
