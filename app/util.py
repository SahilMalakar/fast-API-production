from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

# Hashing (signup)
def hash_password(password: str):
    return pwd_context.hash(password)

# Verification (login)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)