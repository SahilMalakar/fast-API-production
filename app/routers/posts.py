from fastapi import  HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schema import PostCreate , PostUpdate , PostResponse
from app.db import get_db
from app import model

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# 📄 Get single post
@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=PostResponse)
def read_item(id: int, db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = db.fetchone()

    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


# 📚 Get all posts
@router.get("/", status_code=status.HTTP_200_OK,response_model=list[PostResponse])
def read_posts(db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute("SELECT * FROM posts")
    # posts = db.fetchall()

    posts = db.query(model.Post).all()
    return posts


# ➕ Create post
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (payload.title, payload.content, payload.published)
    # )
    # new_post = db.fetchone()
    # connection.commit()

    new_post = model.Post(**payload.dict())
    print(new_post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# 🔄 Update post
@router.put("/{id}", status_code=status.HTTP_200_OK,response_model=PostResponse)
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (payload.title, payload.content, payload.published, id)
    # )
    # updated_post = db.fetchone()

    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

# ❌ Delete post
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute(
    #     "DELETE FROM posts WHERE id = %s RETURNING *",
    #     (id,)
    # )
    # post = db.fetchone()

    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Deleted successfully"}
