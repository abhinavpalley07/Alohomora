from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    owner_name = Column(String, default="Unknown Owner")
    contact_info = Column(String, default="N/A")
    
    # Relationship to notifications
    notifications = relationship("Notification", back_populates="vehicle")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, ACCEPTED, EN_ROUTE
    eta = Column(Integer, nullable=True)  # Estimated time of arrival in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to vehicle
    vehicle = relationship("Vehicle", back_populates="notifications")