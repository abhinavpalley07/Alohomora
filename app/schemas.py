from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Vehicle Schemas ---
class VehicleBase(BaseModel):
    plate_number: str

class VehicleCreate(VehicleBase):
    owner_name: Optional[str] = None
    contact_info: Optional[str] = None

class Vehicle(VehicleBase):
    id: int
    owner_name: str
    contact_info: str

    class Config:
        from_attributes = True

# --- Notification Schemas ---
class NotificationBase(BaseModel):
    vehicle_number: str
    location: str

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(BaseModel):
    id: int
    vehicle_id: int
    location: str
    status: str
    eta: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Request/Response Schemas for specific APIs ---
class OCRRequest(BaseModel):
    image_source: str  # Can be filename or base64 string

class OCRResponse(BaseModel):
    extracted_text: str
    confidence: float

class NearbyParkingRequest(BaseModel):
    latitude: float
    longitude: float

class ParkingSpot(BaseModel):
    name: str
    latitude: float
    longitude: float
    available_spots: int
    distance_km: float

class NotifyRespondRequest(BaseModel):
    notification_id: int
    eta: int  # 2, 5, or 10 minutes