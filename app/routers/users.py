from fastapi import  HTTPException, status, Depends, APIRouter
from app.schema import UserResponse , TokenData
from app.db import get_db
from app import model
from sqlalchemy.orm import Session
from app.util import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get a user by ID
    This endpoint is protected and requires authentication
    """
    print("Current user:", current_user)

    if current_user.user_id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user