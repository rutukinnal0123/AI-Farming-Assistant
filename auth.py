from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from security import verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ----------------------------
# Database Dependency
# ----------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Login Schema
# ----------------------------

class LoginRequest(BaseModel):
    phone: str
    password: str


# ----------------------------
# Login API
# ----------------------------

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    farmer = crud.get_farmer_by_phone(
        db,
        request.phone
    )

    if farmer is None:
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    if not verify_password(
        request.password,
        farmer.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token(
        {
            "sub": str(farmer.id)
        }
    )

    return {

    "access_token": token,

    "token_type": "bearer",

    "farmer": {

        "id": farmer.id,

        "name": farmer.name,

        "phone": farmer.phone,

        "district": farmer.district,

        "village": farmer.village,

        "language": farmer.language

    }

}