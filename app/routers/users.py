from fastapi import  HTTPException, status, Depends, APIRouter
from app.schema import UserCreate , UserResponse
from app.db import get_db
from app import model
from sqlalchemy.orm import Session
from app.util import hash_password, verify_password

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(payload.password)

    user = model.User(
        email=payload.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserResponse)
def login(payload: UserCreate, db: Session = Depends(get_db)):

    user = db.query(model.User).filter(
        model.User.email == payload.email
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    return user



@router.get("/users/{id}",status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user