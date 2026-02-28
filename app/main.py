from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import parking, ocr, notify

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PARKMATE API",
    description="Smart Parking Discovery & Conflict Resolution Platform",
    version="1.0.0"
)

# Configure CORS (Open for hackathon development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
app.include_router(parking.router, prefix="/parking", tags=["Parking Discovery"])
app.include_router(ocr.router, prefix="/ocr", tags=["OCR Scanning"])
app.include_router(notify.router, prefix="/notify", tags=["Notifications"])

@app.get("/")
def root():
    return {"message": "Welcome to PARKMATE API. Visit /docs for documentation."}