import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://unguraladheekshith_db_user:2350T1iazhDPKj2z@cluster0.ejm6xsr.mongodb.net/?retryWrites=true&w=majority"
)

client = AsyncIOMotorClient(MONGO_URI)

db = client["zypark_db"]

def get_db():
    return db