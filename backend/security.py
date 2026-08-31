from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
import crud


# ==========================================================
# PASSWORD HASHING
# ==========================================================

password_hasher = PasswordHasher()


# ==========================================================
# JWT CONFIGURATION
# ==========================================================

SECRET_KEY = "change_this_to_a_long_random_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ==========================================================
# PASSWORD FUNCTIONS
# ==========================================================

def hash_password(password: str):

    return password_hasher.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
):

    try:

        return password_hasher.verify(
            hashed_password,
            plain_password
        )

    except Exception:

        return False


# ==========================================================
# CREATE JWT
# ==========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()


    if expires_delta:

        expire = (
            datetime.utcnow()
            + expires_delta
        )

    else:

        expire = (
            datetime.utcnow()
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
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
# VERIFY JWT
# ==========================================================

def verify_token(
    token: str
):

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


        farmer_id = payload.get(
            "sub"
        )


        if farmer_id is None:

            raise credentials_exception


        return int(
            farmer_id
        )


    except (
        JWTError,
        ValueError,
        TypeError
    ):

        raise credentials_exception


# ==========================================================
# CURRENT LOGGED-IN FARMER
# ==========================================================

def get_current_farmer(

    token: str = Depends(
        oauth2_scheme
    ),

    db: Session = Depends(
        get_db
    )

):

    farmer_id = verify_token(
        token
    )


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
