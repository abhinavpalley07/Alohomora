from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Using SQLite for simple local storage
SQLALCHEMY_DATABASE_URL = "sqlite:///./parkmate.db"

# Create the engine
# check_same_thread is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
Base = declarative_base()

# Dependency to get the DB session in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()