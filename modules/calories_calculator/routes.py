from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from modules.authentication.controller import token_manager
from database_utili.database import get_session
from modules.calories_calculator.controller import total_calories


calories = APIRouter(prefix="/api/v1.0", tags=["Calories Tracker & Calculator"])


@calories.get("/total_calories",status_code=status.HTTP_200_OK)
async def total_calories_daily(
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    
    return total_calories(current_user, db)