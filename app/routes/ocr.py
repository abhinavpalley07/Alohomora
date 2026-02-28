from fastapi import APIRouter
from ..schemas import OCRRequest, OCRResponse
import random

router = APIRouter()

@router.post("/scan", response_model=OCRResponse)
def scan_image(request: OCRRequest):
    """
    Mock OCR API.
    (Logic unchanged)
    """
    if "fail" in request.image_source.lower():
        return OCRResponse(extracted_text="UNKNOWN", confidence=0.0)
    
    mock_plates = ["MH 12 AB 1234", "KA 05 CD 5678", "DL 01 EF 9012"]
    
    return OCRResponse(
        extracted_text=random.choice(mock_plates),
        confidence=random.uniform(0.85, 0.99)
    )