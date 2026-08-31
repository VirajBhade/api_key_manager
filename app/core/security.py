from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from jose import JWTError, jwt
from pwdlib import PasswordHash
import secrets

load_dotenv()



# Configuration


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


# Password Hashing


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)



# JWT


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None



# API Key Hashing
def generate_api_key() -> str:
    return "sk_" + secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    return password_hash.hash(api_key)


def verify_api_key(api_key: str, hashed_api_key: str) -> bool:
    return password_hash.verify(
        api_key,
        hashed_api_key
    )