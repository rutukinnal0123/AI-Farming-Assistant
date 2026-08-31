# ============================================================
# AI FARMING ASSISTANT
# FASTAPI BACKEND
# ============================================================

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Header
)

from sqlalchemy.orm import Session


# ============================================================
# ROUTERS
# ============================================================

from auth import router as auth_router
from chat import router as chat_router
from cnn.routes import router as cnn_router


# ============================================================
# DATABASE / APPLICATION MODULES
# ============================================================

import crud
import models
import schemas

from database import (
    Base,
    SessionLocal,
    engine
)

from security import (
    get_current_farmer
)


# ============================================================
# DATABASE TABLE CREATION
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title="AI Farming Assistant",

    description=(
        "Personal AI Assistant for Farmers"
    ),

    version="1.0.0"
)


# ============================================================
# REGISTER ROUTERS
# ============================================================

app.include_router(
    auth_router
)

app.include_router(
    chat_router
)

app.include_router(
    cnn_router
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "message":
            "Welcome to AI Farming Assistant 🌱"

    }


# ============================================================
# FARMER APIs
# ============================================================

@app.post(
    "/farmers",
    response_model=schemas.FarmerResponse
)
def create_farmer(

    farmer: schemas.FarmerCreate,

    authorization: str | None = Header(
        default=None
    ),

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------------------------------
    # PREVENT REGISTRATION WHILE LOGGED IN
    # --------------------------------------------------------

    if authorization is not None:

        raise HTTPException(

            status_code=400,

            detail=(
                "You are already logged in. "
                "Please logout before registering "
                "a new farmer."
            )

        )


    # --------------------------------------------------------
    # CHECK EXISTING PHONE
    # --------------------------------------------------------

    existing = crud.get_farmer_by_phone(
        db,
        farmer.phone
    )


    if existing:

        raise HTTPException(

            status_code=400,

            detail=(
                "Phone number already registered."
            )

        )


    return crud.create_farmer(
        db,
        farmer
    )


# ============================================================
# GET ALL FARMERS
# ============================================================

@app.get("/farmers")
def get_all_farmers(

    db: Session = Depends(
        get_db
    )

):

    return crud.get_all_farmers(
        db
    )


# ============================================================
# GET FARMER
# ============================================================

@app.get(
    "/farmers/{farmer_id}"
)
def get_farmer(

    farmer_id: int,

    db: Session = Depends(
        get_db
    )

):

    farmer = crud.get_farmer(
        db,
        farmer_id
    )


    if not farmer:

        raise HTTPException(

            status_code=404,

            detail="Farmer not found."

        )


    return farmer


# ============================================================
# FARM APIs
# ============================================================

@app.post(
    "/farms",
    response_model=schemas.FarmResponse
)
def create_farm(

    farm: schemas.FarmCreate,

    current_farmer=Depends(
        get_current_farmer
    ),

    db: Session = Depends(
        get_db
    )

):

    farm_data = farm.model_dump()

    farm_data["farmer_id"] = (
        current_farmer.id
    )


    db_farm = models.Farm(
        **farm_data
    )


    db.add(
        db_farm
    )

    db.commit()

    db.refresh(
        db_farm
    )


    return db_farm


# ============================================================
# GET ALL FARMS
# ============================================================

@app.get("/farms")
def get_all_farms(

    db: Session = Depends(
        get_db
    )

):

    return crud.get_all_farms(
        db
    )


# ============================================================
# GET FARMER FARMS
# ============================================================

@app.get(
    "/farmers/{farmer_id}/farms"
)
def get_farmer_farms(

    farmer_id: int,

    db: Session = Depends(
        get_db
    )

):

    return crud.get_farmer_farms(
        db,
        farmer_id
    )


# ============================================================
# ACTIVITY APIs
# ============================================================

@app.post(
    "/activities",
    response_model=schemas.ActivityResponse
)
def create_activity(

    activity: schemas.ActivityCreate,

    db: Session = Depends(
        get_db
    )

):

    farm = crud.get_farm(
        db,
        activity.farm_id
    )


    if not farm:

        raise HTTPException(

            status_code=404,

            detail="Farm not found."

        )


    return crud.create_activity(
        db,
        activity
    )


# ============================================================
# GET FARM ACTIVITIES
# ============================================================

@app.get(
    "/farms/{farm_id}/activities"
)
def get_farm_activities(

    farm_id: int,

    db: Session = Depends(
        get_db
    )

):

    return crud.get_farm_activities(
        db,
        farm_id
    )


# ============================================================
# REMINDER APIs
# ============================================================

@app.post(
    "/reminders",
    response_model=schemas.ReminderResponse
)
def create_reminder(

    reminder: schemas.ReminderCreate,

    db: Session = Depends(
        get_db
    )

):

    farm = crud.get_farm(
        db,
        reminder.farm_id
    )


    if not farm:

        raise HTTPException(

            status_code=404,

            detail="Farm not found."

        )


    return crud.create_reminder(
        db,
        reminder
    )


# ============================================================
# GET FARM REMINDERS
# ============================================================

@app.get(
    "/farms/{farm_id}/reminders"
)
def get_farm_reminders(

    farm_id: int,

    db: Session = Depends(
        get_db
    )

):

    return crud.get_farm_reminders(
        db,
        farm_id
    )


# ============================================================
# CHAT HISTORY APIs
# ============================================================

@app.post(
    "/chat-history",
    response_model=schemas.ChatHistoryResponse
)
def save_chat(

    chat: schemas.ChatHistoryCreate,

    db: Session = Depends(
        get_db
    )

):

    farmer = crud.get_farmer(
        db,
        chat.farmer_id
    )


    if not farmer:

        raise HTTPException(

            status_code=404,

            detail="Farmer not found."

        )


    return crud.save_chat(
        db,
        chat
    )


# ============================================================
# GET CHAT HISTORY
# ============================================================

@app.get(
    "/farmers/{farmer_id}/chat-history"
)
def get_chat_history(

    farmer_id: int,

    db: Session = Depends(
        get_db
    )

):

    return crud.get_chat_history(
        db,
        farmer_id
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )
