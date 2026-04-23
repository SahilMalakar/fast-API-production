from app.schema import UserResponse
from fastapi import status, Depends, APIRouter
from app import model
from app.util import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me",status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
    current_user: model.User = Depends(get_current_user)
):
    """
    Get the currently logged-in user's details
    This endpoint requires authentication
    """
    return current_user