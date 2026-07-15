from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# ============================================================
# FARMER
# ============================================================

class FarmerBase(BaseModel):
    name: str
    phone: str
    password: str
    district: str
    village: str
    language: str = "Malayalam"


class FarmerCreate(FarmerBase):
    pass


class FarmerResponse(BaseModel):
    id: int
    name: str
    phone: str
    district: str
    village: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# FARM
# ============================================================

class FarmCreate(BaseModel):
    farm_name: str
    crop: str
    crop_stage: str = "Seedling"
    land_size: float
    soil_type: str
    irrigation: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FarmResponse(BaseModel):
    id: int
    farmer_id: int
    farm_name: str
    crop: str
    crop_stage: str
    land_size: float
    soil_type: str
    irrigation: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# ACTIVITY
# ============================================================

class ActivityBase(BaseModel):
    farm_id: int
    activity_type: str
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    activity_date: Optional[date] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# REMINDER
# ============================================================

class ReminderBase(BaseModel):
    farm_id: int
    title: str
    message: Optional[str] = None
    due_date: Optional[date] = None
    status: str = "Pending"


class ReminderCreate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# CHAT HISTORY
# ============================================================

class ChatHistoryBase(BaseModel):
    farmer_id: int
    question: str
    answer: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistoryResponse(ChatHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True