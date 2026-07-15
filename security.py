from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
import crud


# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = "change_this_to_a_long_random_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================================
# Database Dependency
# ==========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Password Functions
# ==========================================================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================================
# Create JWT
# ==========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================================================
# Verify JWT
# ==========================================================

def verify_token(token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token."
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        farmer_id = payload.get("sub")

        if farmer_id is None:
            raise credentials_exception

        return int(farmer_id)

    except JWTError:
        raise credentials_exception


# ==========================================================
# Current Logged-in Farmer
# ==========================================================

def get_current_farmer(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    farmer_id = verify_token(token)

    farmer = crud.get_farmer(
        db,
        farmer_id
    )

    if farmer is None:

        raise HTTPException(
            status_code=404,
            detail="Farmer not found."
        )

    return farmer