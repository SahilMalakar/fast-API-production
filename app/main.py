from fastapi import FastAPI, status
from app import model
from app.db import engine
from app.routers import posts , users , auth ,votes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Social media app",
    description="social media application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


origins = [
    "http://localhost:3000",   # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE etc.
    allow_headers=["*"],            # Authorization, Content-Type etc.
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

# 🏠 Health check
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "welcome to the API"}