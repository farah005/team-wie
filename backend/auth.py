from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY non définie dans le fichier .env")

ALGORITHM = "HS256"

fake_users = {
    "societe_sport":   {"password": "sport123", "interest": "sports"},
    "marque_mode":     {"password": "mode123",  "interest": "fashion"},
    "entreprise_tech": {"password": "tech123",  "interest": "tech"},
    "journaliste":     {"password": "news123",  "interest": "general"}
}

def authenticate_user(username: str, password: str):
    user = fake_users.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None