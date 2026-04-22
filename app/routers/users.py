from fastapi import  HTTPException, status, Depends, APIRouter
from app.schema import UserResponse
from app.db import get_db
from app import model
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user