from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_ ,func

from app.schema import PostCreate, PostUpdate, PostResponse , PostResponseWithVotes
from app.db import get_db
from app import model
from app.util import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# 📄 Get single post (ONLY OWNER)
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseWithVotes)
def read_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    result = db.query(
        model.Post,
        func.count(model.Vote.post_id).label("votes")
    ).join(
        model.Vote,
        model.Vote.post_id == model.Post.id,
        isouter=True
    ).group_by(
        model.Post.id
    ).filter(
        model.Post.id == id,
        model.Post.user_id == current_user.id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, votes = result

    return {
        "post": post,
        "votes": votes
    }

# 📚 Get all posts (ONLY USER'S POSTS + PAGINATION)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponseWithVotes])
def read_posts(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
    limit: int = Query(10, le=100),
    skip: int = Query(0, ge=0),
    search: str | None = None
):
    query = db.query(
        model.Post,
        func.count(model.Vote.post_id).label("votes")
    ).join(
        model.Vote,
        model.Vote.post_id == model.Post.id,
        isouter=True
    ).group_by(
        model.Post.id
    ).filter(
        model.Post.user_id == current_user.id
    )

    # 🔍 Search
    if search:
        query = query.filter(
            or_(
                model.Post.title.ilike(f"%{search}%"),
                model.Post.content.ilike(f"%{search}%")
            )
        )

    results = query.limit(limit).offset(skip).all()


    return [{
        "post": post,
        "votes": votes
    } 
    for post, votes in results]

# ➕ Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    new_post = model.Post(
        **payload.dict(),
        user_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# 🔄 Update post (ONLY OWNER)
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(
    id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    post_query = db.query(model.Post).filter(
        model.Post.id == id,
        model.Post.user_id == current_user.id
    )

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_query.update(
        payload.dict(exclude_unset=True),
        synchronize_session=False
    )
    db.commit()

    return post_query.first()


# ❌ Delete post (ONLY OWNER)
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    post_query = db.query(model.Post).filter(
        model.Post.id == id,
        model.Post.user_id == current_user.id
    )

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Deleted successfully"}