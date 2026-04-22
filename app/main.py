from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import model
from app.db import engine, get_db
from app.schema import PostCreate



# 🔌 Establish DB connection with retry (useful if DB starts late)
# while True:
#     try:
#         connection = psycopg.connect(
#             host="localhost",
#             user="postgres",
#             password="sweety@12345",
#             dbname="fastapi",
#             port=5432,
#             row_factory=dict_row  # return rows as dict instead of tuple
#         )
#         db = connection.cursor()

#         db.execute("SELECT NOW()")
#         print("Connected to DB:", db.fetchone())
#         break

#     except Exception as e:
#         print("DB connection failed:", e)
#         sleep(3)

# Create tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🏠 Health check
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "welcome to the API"}


# 📄 Get single post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
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
@app.get("/posts", status_code=status.HTTP_200_OK)
def read_posts(db: Session = Depends(get_db)):

    # RAW SQL (COMMENTED)
    # db.execute("SELECT * FROM posts")
    # posts = db.fetchall()

    posts = db.query(model.Post).all()
    return {"posts": posts}


# ➕ Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, payload: PostCreate, db: Session = Depends(get_db)):

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
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

    return