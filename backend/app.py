from fastapi import FastAPI, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from auth import router as auth_router
from chat import router as chat_router
import crud
import models
import schemas

from database import Base, SessionLocal, engine
from security import get_current_farmer



# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Farming Assistant",
    description="Personal AI Assistant for Farmers",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(chat_router)

# ===========================================================
# Database Dependency
# ===========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===========================================================
# Home
# ===========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Farming Assistant 🌱"
    }


# ===========================================================
# Farmer APIs
# ===========================================================

@app.post("/farmers", response_model=schemas.FarmerResponse)
def create_farmer(
    farmer: schemas.FarmerCreate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):

    # If the request already contains a login token,
    # force the user to logout first.
    if authorization is not None:

        raise HTTPException(
            status_code=400,
            detail="You are already logged in. Please logout before registering a new farmer."
        )

    existing = crud.get_farmer_by_phone(db, farmer.phone)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered."
        )

    return crud.create_farmer(db, farmer)


@app.get("/farmers")
def get_all_farmers(
        db: Session = Depends(get_db)
):
    return crud.get_all_farmers(db)


@app.get("/farmers/{farmer_id}")
def get_farmer(
        farmer_id: int,
        db: Session = Depends(get_db)
):

    farmer = crud.get_farmer(db, farmer_id)

    if not farmer:
        raise HTTPException(
            status_code=404,
            detail="Farmer not found."
        )

    return farmer


# ===========================================================
# Farm APIs
# ===========================================================

@app.post("/farms", response_model=schemas.FarmResponse)
def create_farm(
    farm: schemas.FarmCreate,
    current_farmer=Depends(get_current_farmer),
    db: Session = Depends(get_db)
):

    farm_data = farm.model_dump()

    farm_data["farmer_id"] = current_farmer.id

    db_farm = models.Farm(**farm_data)

    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)

    return db_farm


@app.get("/farms")
def get_all_farms(
        db: Session = Depends(get_db)
):
    return crud.get_all_farms(db)


@app.get("/farmers/{farmer_id}/farms")
def get_farmer_farms(
        farmer_id: int,
        db: Session = Depends(get_db)
):

    return crud.get_farmer_farms(db, farmer_id)


# ===========================================================
# Activity APIs
# ===========================================================

@app.post(
    "/activities",
    response_model=schemas.ActivityResponse
)
def create_activity(
        activity: schemas.ActivityCreate,
        db: Session = Depends(get_db)
):

    farm = crud.get_farm(db, activity.farm_id)

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found."
        )

    return crud.create_activity(db, activity)


@app.get("/farms/{farm_id}/activities")
def get_farm_activities(
        farm_id: int,
        db: Session = Depends(get_db)
):

    return crud.get_farm_activities(db, farm_id)


# ===========================================================
# Reminder APIs
# ===========================================================

@app.post(
    "/reminders",
    response_model=schemas.ReminderResponse
)
def create_reminder(
        reminder: schemas.ReminderCreate,
        db: Session = Depends(get_db)
):

    farm = crud.get_farm(db, reminder.farm_id)

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found."
        )

    return crud.create_reminder(db, reminder)


@app.get("/farms/{farm_id}/reminders")
def get_farm_reminders(
        farm_id: int,
        db: Session = Depends(get_db)
):

    return crud.get_farm_reminders(db, farm_id)


# ===========================================================
# Chat History APIs
# ===========================================================

@app.post(
    "/chat-history",
    response_model=schemas.ChatHistoryResponse
)
def save_chat(
        chat: schemas.ChatHistoryCreate,
        db: Session = Depends(get_db)
):

    farmer = crud.get_farmer(db, chat.farmer_id)

    if not farmer:
        raise HTTPException(
            status_code=404,
            detail="Farmer not found."
        )

    return crud.save_chat(db, chat)


@app.get("/farmers/{farmer_id}/chat-history")
def get_chat_history(
        farmer_id: int,
        db: Session = Depends(get_db)
):

    return crud.get_chat_history(db, farmer_id)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )