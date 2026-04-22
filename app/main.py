from fastapi import FastAPI, status
from app import model
from app.db import engine
from app.routers import posts , users , auth

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# 🏠 Health check
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "welcome to the API"}