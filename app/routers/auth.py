from fastapi import  HTTPException, status, Depends, APIRouter , Response
from fastapi.security import OAuth2PasswordRequestForm
from app.schema import UserCreate , AuthResponse
from app.db import get_db
from app import model
from sqlalchemy.orm import Session
from app.util import hash_password, verify_password
from app.util import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup",status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
def signup(
    payload: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):

    existing_user = db.query(model.User).filter(
        model.User.email == payload.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = hash_password(payload.password)

    user = model.User(
        email=payload.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {
        "message": "User created successfully",
        "user": user
    }

@router.post("/login",status_code=status.HTTP_200_OK, response_model=AuthResponse)
def login(
    payload: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,
    db: Session = Depends(get_db)
):

    user = db.query(model.User).filter(
        model.User.email == payload.username   
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=403,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {
        "message": "User logged in successfully",
        "user": user
    }