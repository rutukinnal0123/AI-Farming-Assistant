
from sqlalchemy.orm import Session
from security import hash_password

import models
import schemas


# ==========================================================
# FARMER CRUD
# ==========================================================

def create_farmer(db: Session, farmer: schemas.FarmerCreate):

    farmer_data = farmer.model_dump()

    farmer_data["password"] = hash_password(
        farmer.password
    )

    db_farmer = models.Farmer(**farmer_data)

    db.add(db_farmer)

    db.commit()

    db.refresh(db_farmer)

    return db_farmer


def get_farmer(db: Session, farmer_id: int):
    return db.query(models.Farmer).filter(
        models.Farmer.id == farmer_id
    ).first()


def get_farmer_by_phone(db: Session, phone: str):
    return db.query(models.Farmer).filter(
        models.Farmer.phone == phone
    ).first()


def get_all_farmers(db: Session):
    return db.query(models.Farmer).all()


def update_farmer(db: Session, farmer_id: int, updated_data: schemas.FarmerCreate):
    farmer = get_farmer(db, farmer_id)

    if farmer:
        for key, value in updated_data.model_dump().items():
            setattr(farmer, key, value)

        db.commit()
        db.refresh(farmer)

    return farmer


def delete_farmer(db: Session, farmer_id: int):
    farmer = get_farmer(db, farmer_id)

    if farmer:
        db.delete(farmer)
        db.commit()

    return farmer


# ==========================================================
# FARM CRUD
# ==========================================================

def create_farm(db: Session, farm: schemas.FarmCreate):
    db_farm = models.Farm(**farm.model_dump())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm


def get_farm(db: Session, farm_id: int):
    return db.query(models.Farm).filter(
        models.Farm.id == farm_id
    ).first()


def get_all_farms(db: Session):
    return db.query(models.Farm).all()


def get_farmer_farms(db: Session, farmer_id: int):
    return db.query(models.Farm).filter(
        models.Farm.farmer_id == farmer_id
    ).all()


# ==========================================================
# ACTIVITY CRUD
# ==========================================================

def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(
        models.Activity.id == activity_id
    ).first()


def get_farm_activities(db: Session, farm_id: int):
    return db.query(models.Activity).filter(
        models.Activity.farm_id == farm_id
    ).all()


# ==========================================================
# REMINDER CRUD
# ==========================================================

def create_reminder(db: Session, reminder: schemas.ReminderCreate):
    db_reminder = models.Reminder(**reminder.model_dump())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def get_farm_reminders(db: Session, farm_id: int):
    return db.query(models.Reminder).filter(
        models.Reminder.farm_id == farm_id
    ).all()


# ==========================================================
# CHAT HISTORY CRUD
# ==========================================================

def save_chat(db: Session, chat: schemas.ChatHistoryCreate):
    db_chat = models.ChatHistory(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat_history(db: Session, farmer_id: int):
    return db.query(models.ChatHistory).filter(
        models.ChatHistory.farmer_id == farmer_id
    ).order_by(
        models.ChatHistory.created_at.desc()
    ).all()