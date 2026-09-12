import os
from datetime import datetime, timedelta
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-.env")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24h default

bearer_scheme = HTTPBearer()

# Pre-hashed default for Admin@Atharva2026!
DEFAULT_ADMIN_HASH = "$2b$12$DaZZ4Hknt2bZS/X2Xf4mK.B.PCufvXZEeKF57FdC0wN1jvZiQ8Hje"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_admin_password(password: str) -> bool:
    admin_hash = os.getenv("ADMIN_PASSWORD_HASH") or DEFAULT_ADMIN_HASH
    try:
        return bcrypt.checkpw(password.encode("utf-8"), admin_hash.strip().encode("utf-8"))
    except Exception:
        return False


def create_access_token() -> str:
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": "admin", "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("sub") != "admin":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return True
