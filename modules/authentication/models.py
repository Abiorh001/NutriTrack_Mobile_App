from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Text
from sqlalchemy.orm import relationship, backref
from database_utili.database import Base
import uuid
from datetime import datetime




#table for user
class User(Base):
    __tablename__ = "user"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(225), nullable=False)
    address = Column(String(300), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    DOB = Column(Date, nullable=False)
    phone_number = Column(Integer, nullable=False)
    dietary_preference = Column(String(300))
    fitness_goal = Column(String(300))
    medical_condition = Column(Text)
    email_confirmation_token = Column(String(128), default=None)
    reset_token = Column(String(128), default=None)
    date_created= Column(DateTime, default=datetime.utcnow)
    date_updated= Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="user")
    food_logs = relationship("FoodLogging", backref="user", cascade="all, delete", passive_deletes=True)


#table for revoked token from our jwt token when
class RevokedToken(Base):
    __tablename__ = 'revoked_token'

    id = Column(String(225), primary_key=True)


