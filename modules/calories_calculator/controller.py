from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from modules.authentication.controller import token_manager
from database_utili.database import get_session
from modules.authentication.models import User
from datetime import date




#function to get all total calories for the day
def total_calories(current_user:str = Depends(token_manager),
                   db:Session = Depends(get_session)):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # today = date.today()
    # total_calories = (
    #     db.query(func.sum(Entry.calories))
    #     .filter(func.DATE(Entry.date) == today, Entry.users_id == existing_user.id)
    #     .scalar()
    # )

    return {"total calories": total_calories}
