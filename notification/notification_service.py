from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI(title="Corporate Notification Service")

# SQLAlchemy setup
DATABASE_URL = (
    "mssql+pyodbc://admin:nkol6056@"
    "meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com:1433/meditrackDB?"
    "driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Notification DB Model
class Notification(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'schema': 'common'}

    notification_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False, default="Pending")

# Pydantic Schemas
class NotificationCreate(BaseModel):
    member_email: EmailStr
    message: str
    sent_at: Optional[datetime] = datetime.utcnow()
    status: Optional[str] = "Pending"

class NotificationOut(BaseModel):
    notification_id: int
    member_email: str
    message: str
    sent_at: datetime
    status: str

    class Config:
        orm_mode = True

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables (run once, or with Alembic for migrations)
# Base.metadata.create_all(bind=engine)

# GET notifications
@app.get("/notifications", response_model=List[NotificationOut])
def get_notifications(email: Optional[str] = Query(None), db: SessionLocal = next(get_db())):
    if email:
        notifications = db.query(Notification).filter(Notification.member_email == email).all()
        if not notifications:
            raise HTTPException(status_code=404, detail="No notifications found for the provided email.")
        return notifications
    return db.query(Notification).all()

# POST a new notification
@app.post("/notifications", response_model=dict, status_code=201)
def create_notification(notification: NotificationCreate, db: SessionLocal = next(get_db())):
    db_notification = Notification(
        member_email=notification.member_email,
        message=notification.message,
        sent_at=notification.sent_at,
        status=notification.status,
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return {"message": "Notification created successfully."}
