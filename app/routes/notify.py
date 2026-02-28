from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vehicle, Notification
from ..schemas import NotificationCreate, NotificationResponse, NotifyRespondRequest

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    """
    Create a notification entry. 
    If vehicle doesn't exist, create it on the fly (Mock logic).
    """
    # Check if vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.plate_number == notification.vehicle_number).first()
    
    if not vehicle:
        # Create mock vehicle if not found
        vehicle = Vehicle(
            plate_number=notification.vehicle_number, 
            owner_name="Unknown Owner",
            contact_info="Not Registered"
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)

    # Create notification
    new_notification = Notification(
        vehicle_id=vehicle.id,
        location=notification.location,
        status="PENDING"
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    
    return new_notification

@router.post("/respond", response_model=NotificationResponse)
def respond_to_notification(response: NotifyRespondRequest, db: Session = Depends(get_db)):
    """
    Update notification status with ETA.
    """
    # Validate ETA
    if response.eta not in [2, 5, 10]:
        raise HTTPException(status_code=400, detail="ETA must be 2, 5, or 10 minutes")

    notification = db.query(Notification).filter(Notification.id == response.notification_id).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.status = "EN_ROUTE"
    notification.eta = response.eta
    
    db.commit()
    db.refresh(notification)
    
    return notification