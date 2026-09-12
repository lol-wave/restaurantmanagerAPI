from bcrypt import checkpw, hashpw, gensalt
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def hash_password(password: str) -> str:
    hashed = hashpw(password, gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password, hashed_password)

def create_access_token(user_id: int, secret_key: str, algorithm= ALGORITHM) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(data, secret_key, algorithm=algorithm)