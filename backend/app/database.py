# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - start with SQLite for simplicity
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./baby_ai.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.relationship import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    babies = relationship("Baby", back_populates="user")

class Baby(Base):
    __tablename__ = "babies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="babies")
    interactions = relationship("UserActivityInteraction", back_populates="baby")
    milestones = relationship("Milestone", back_populates="baby")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    age_min_months = Column(Integer, nullable=False)
    age_max_months = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)  # motor, cognitive, social, sensory
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    duration_minutes = Column(Integer, default=15)
    materials_needed = Column(Text)
    instructions = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interactions = relationship("UserActivityInteraction", back_populates="activity")

class UserActivityInteraction(Base):
    __tablename__ = "user_activity_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    baby_id = Column(Integer, ForeignKey("babies.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    interaction_type = Column(String(20), nullable=False)  # viewed, started, completed, skipped
    rating = Column(Integer)  # 1-5 stars if completed
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    baby = relationship("Baby", back_populates="interactions")
    activity = relationship("Activity", back_populates="interactions")

class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    baby_id = Column(Integer, ForeignKey("babies.id"), nullable=False)
    milestone_type = Column(String(100), nullable=False)
    achieved_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    baby = relationship("Baby", back_populates="milestones")

# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Baby schemas
class BabyBase(BaseModel):
    name: str
    birth_date: date
    gender: Optional[str] = None

class BabyCreate(BabyBase):
    pass

class BabyResponse(BabyBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    age_min_months: int
    age_max_months: int
    category: str
    difficulty_level: int = 1
    duration_minutes: int = 15
    materials_needed: Optional[str] = None
    instructions: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Recommendation schema
class RecommendationResponse(BaseModel):
    activity: ActivityResponse
    score: float
    reason: str

# Interaction schemas
class InteractionCreate(BaseModel):
    activity_id: int
    interaction_type: str  # viewed, started, completed, skipped
    rating: Optional[int] = None
    notes: Optional[str] = None

class InteractionResponse(BaseModel):
    id: int
    baby_id: int
    activity_id: int
    interaction_type: str
    rating: Optional[int]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Milestone schemas
class MilestoneCreate(BaseModel):
    milestone_type: str
    achieved_date: Optional[date] = None
    notes: Optional[str] = None

class MilestoneResponse(BaseModel):
    id: int
    baby_id: int
    milestone_type: str
    achieved_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
