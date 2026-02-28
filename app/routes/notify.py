from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from typing import List

from ..database import get_db
from ..schemas import NotificationCreate, NotificationResponse, NotifyRespondRequest

router = APIRouter()

def notification_helper(notification) -> dict:
    """
    Helper to format MongoDB document for response.
    Converts ObjectId to string and maps fields.
    """
    return {
        "id": str(notification["_id"]),
        "vehicle_number": notification["vehicle_number"],
        "location": notification["location"],
        "status": notification["status"],
        "eta": notification.get("eta"),
        "created_at": notification["created_at"]
    }

@router.post("/", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate, db = Depends(get_db)):
    """
    Create notification. Creates vehicle if not exists.
    """
    vehicles_collection = db["vehicles"]
    notifications_collection = db["notifications"]

    # Check if vehicle exists
    vehicle = await vehicles_collection.find_one({"plate_number": notification.vehicle_number})
    
    if not vehicle:
        # Insert mock vehicle
        new_vehicle = {
            "plate_number": notification.vehicle_number,
            "owner_name": "Unknown Owner",
            "contact_info": "Not Registered"
        }
        await vehicles_collection.insert_one(new_vehicle)

    # Create notification document
    new_notification = {
        "vehicle_number": notification.vehicle_number,
        "location": notification.location,
        "status": "PENDING",
        "eta": None,
        "created_at": datetime.utcnow()
    }
    
    result = await notifications_collection.insert_one(new_notification)
    created_doc = await notifications_collection.find_one({"_id": result.inserted_id})
    
    return notification_helper(created_doc)

@router.post("/respond", response_model=NotificationResponse)
async def respond_to_notification(response: NotifyRespondRequest, db = Depends(get_db)):
    """
    Update notification status with ETA.
    """
    if response.eta not in [2, 5, 10]:
        raise HTTPException(status_code=400, detail="ETA must be 2, 5, or 10 minutes")

    notifications_collection = db["notifications"]
    
    # Convert string ID to ObjectId for query
    try:
        oid = ObjectId(response.notification_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Update the document
    update_result = await notifications_collection.update_one(
        {"_id": oid}, 
        {"$set": {"status": "EN_ROUTE", "eta": response.eta}}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    updated_doc = await notifications_collection.find_one({"_id": oid})
    return notification_helper(updated_doc)