from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg://postgres:sweety%4012345@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL,echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()