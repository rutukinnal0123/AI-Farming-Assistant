from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    DateTime,
    Text
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime


# ==========================================================
# FARMER
# ==========================================================

class Farmer(Base):

    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    phone = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    district = Column(String, nullable=False)

    village = Column(String, nullable=False)

    language = Column(String, default="Malayalam")

    created_at = Column(DateTime, default=datetime.utcnow)

    farms = relationship(
        "Farm",
        back_populates="farmer",
        cascade="all, delete"
    )

    chats = relationship(
        "ChatHistory",
        back_populates="farmer",
        cascade="all, delete"
    )


# ==========================================================
# FARM
# ==========================================================

class Farm(Base):

    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)

    farmer_id = Column(
        Integer,
        ForeignKey("farmers.id")
    )

    farm_name = Column(String, nullable=False)

    crop = Column(String, nullable=False)

    crop_stage = Column(
        String,
        default="Seedling"
    )

    land_size = Column(Float)

    soil_type = Column(String)

    irrigation = Column(String)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    farmer = relationship(
        "Farmer",
        back_populates="farms"
    )

    activities = relationship(
        "Activity",
        back_populates="farm",
        cascade="all, delete"
    )

    reminders = relationship(
        "Reminder",
        back_populates="farm",
        cascade="all, delete"
    )


# ==========================================================
# ACTIVITY
# ==========================================================

class Activity(Base):

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(
        Integer,
        ForeignKey("farms.id")
    )

    activity_type = Column(String)

    description = Column(Text)

    quantity = Column(Float, nullable=True)

    unit = Column(String, nullable=True)

    activity_date = Column(
        Date,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    farm = relationship(
        "Farm",
        back_populates="activities"
    )


# ==========================================================
# REMINDER
# ==========================================================

class Reminder(Base):

    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(
        Integer,
        ForeignKey("farms.id")
    )

    title = Column(String)

    message = Column(Text)

    due_date = Column(
        Date,
        nullable=True
    )

    status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    farm = relationship(
        "Farm",
        back_populates="reminders"
    )


# ==========================================================
# CHAT HISTORY
# ==========================================================

class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    farmer_id = Column(
        Integer,
        ForeignKey("farmers.id")
    )

    question = Column(Text)

    answer = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    farmer = relationship(
        "Farmer",
        back_populates="chats"
    )