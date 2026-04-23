from app.schema import VoteBase
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app import model
from app.util import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: VoteBase,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check if post exist
    post = db.query(model.Post).filter(
        model.Post.id == vote.post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    # 2. Check if vote already exists
    existing_vote = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id,
        model.Vote.user_id == current_user.id
    ).first()

    # UPVOTE
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post"
            )

        new_vote = model.Vote(
            post_id=vote.post_id,
            user_id=current_user.id
        )

        db.add(new_vote)
        db.commit()

        return {"message": "Vote added successfully"}

    # REMOVE VOTE
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )

        db.delete(existing_vote)
        db.commit()

        return {"message": "Vote removed successfully"}