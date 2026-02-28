from fastapi import APIRouter, Depends
from typing import List
from ..schemas import NearbyParkingRequest, ParkingSpot
import math

router = APIRouter()

# Mock function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    return round(math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111, 2)

@router.post("/nearby", response_model=List[ParkingSpot])
def get_nearby_parking(request: NearbyParkingRequest):
    """
    Mock API to return nearby parking spots based on lat/long.
    (Logic unchanged as it uses mock data)
    """
    mock_spots = [
        {"name": "Central Mall Parking", "lat": request.latitude + 0.01, "lon": request.longitude + 0.01, "available": 5},
        {"name": "Street Side Spot A", "lat": request.latitude - 0.005, "lon": request.longitude + 0.002, "available": 1},
        {"name": "Tech Park Garage", "lat": request.latitude + 0.02, "lon": request.longitude - 0.01, "available": 12},
    ]
    
    results = []
    for spot in mock_spots:
        dist = calculate_distance(request.latitude, request.longitude, spot["lat"], spot["lon"])
        results.append(ParkingSpot(
            name=spot["name"],
            latitude=spot["lat"],
            longitude=spot["lon"],
            available_spots=spot["available"],
            distance_km=dist
        ))
    
    results.sort(key=lambda x: x.distance_km)
    return results