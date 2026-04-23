from app import model
from datetime import timedelta , datetime
from jwt import encode, decode ,InvalidTokenError , ExpiredSignatureError
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app.db import get_db
from app.schema import TokenData
from fastapi import Cookie, Depends, HTTPException
from starlette import status

pwd_context = PasswordHash.recommended()

# Hashing (signup)
def hash_password(password: str):
    return pwd_context.hash(password)

# Verification (login)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



# secret key
SECRET_KEY = "my_secret_key_345678uytrsxcvbj098765qwergcbnjo09876543"
# Access token lifetime
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Algorithm
ALGORITHM = "HS256"


# create token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print("expiry time:",expire)

    to_encode.update({"exp": expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# decode token
def verify_access_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return TokenData(user_id=user_id, email=email)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_user(access_token: str = Cookie(None),db: Session = Depends(get_db)):

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token_data = verify_access_token(access_token)
    user = db.query(model.User).filter(model.User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    return user