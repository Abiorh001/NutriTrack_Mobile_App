from pydantic import BaseModel
from typing import Optional

class FoodLoggingCreate(BaseModel):
    id: Optional[str]
    food_name: Optional[str]
    brand_name: Optional[str]
    serving_qty: Optional[float]
    serving_unit: Optional[str]
    serving_weight_grams: Optional[float]
    calories: Optional[float]
    total_fat: Optional[float]
    saturated_fat: Optional[float]
    cholesterol: Optional[float]
    sodium: Optional[float]
    total_carbohydrate: Optional[float]
    dietary_fiber: Optional[float]
    sugars: Optional[float]
    protein: Optional[float]
    potassium: Optional[float]
    p: Optional[float]
    is_raw_food: Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True
