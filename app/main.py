from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import parking, ocr, notify

app = FastAPI(
    title="ZYPARK API",
    description="Smart Parking Discovery & Conflict Resolution Platform (MongoDB)",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(parking.router, prefix="/parking", tags=["Parking Discovery"])
app.include_router(ocr.router, prefix="/ocr", tags=["OCR Scanning"])
app.include_router(notify.router, prefix="/notify", tags=["Notifications"])

@app.get("/")
def root():
    return {"message": "Welcome to ZYPARK API (MongoDB Edition). Visit /docs for documentation."}