from jwt import PyJWTError
from starlette import status
from fastapi import HTTPException
from datetime import timedelta , datetime
from pwdlib import PasswordHash
from jwt import encode, decode


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
def decode_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print(payload)
        return payload

    except PyJWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )