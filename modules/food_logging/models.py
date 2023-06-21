from sqlalchemy import Column, Float, String, ForeignKey, DateTime, Date
from database_utili.database import Base
import uuid
from datetime import datetime, date




class FoodLogging(Base):
    __tablename__ = 'food_log'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    food_name = Column(String)
    brand_name = Column(String)
    serving_qty = Column(Float)
    serving_unit = Column(String)
    serving_weight_grams = Column(Float)
    calories = Column(Float)
    total_fat = Column(Float)
    saturated_fat = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    total_carbohydrate = Column(Float)
    dietary_fiber = Column(Float)
    sugars = Column(Float)
    protein = Column(Float)
    potassium = Column(Float)
    p = Column(Float)
    is_raw_food = Column(String)
    user_id = Column(String, ForeignKey("user.id"))
    date_created= Column(DateTime, default=datetime.utcnow)
    date_updated= Column(DateTime, default=datetime.utcnow)
    date = Column(Date, default=date.today)
   


