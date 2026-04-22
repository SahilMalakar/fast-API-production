from time import sleep
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

app = FastAPI()


# 📦 Request body schema (validation + deserialization)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# 🔌 Establish DB connection with retry (useful if DB starts late)
while True:
    try:
        connection = psycopg.connect(
            host="localhost",
            user="postgres",
            password="sweety@12345",
            dbname="fastapi",
            port=5432,
            row_factory=dict_row  # return rows as dict instead of tuple
        )
        db = connection.cursor()

        db.execute("SELECT NOW()")
        print("Connected to DB:", db.fetchone())
        break

    except Exception as e:
        print("DB connection failed:", e)
        sleep(3)


# 🏠 Health check route
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "welcome to the API"}


# 📄 Get single post by ID
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def read_item(id: int):
    db.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = db.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


# 📚 Get all posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def read_posts():
    db.execute("SELECT * FROM posts")
    posts = db.fetchall()

    return {"posts": posts}


# ➕ Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    # Use parameterized query to prevent SQL injection
    db.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (payload.title, payload.content, payload.published)
    )

    new_post = db.fetchone()
    connection.commit()  # persist changes

    return new_post


# 🔄 Update existing post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, payload: Post):
    db.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (payload.title, payload.content, payload.published, id)
    )

    updated_post = db.fetchone()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    connection.commit()
    return updated_post


# ❌ Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    db.execute(
        "DELETE FROM posts WHERE id = %s RETURNING *",
        (id,)
    )

    post = db.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    connection.commit()
    return