from fastapi import HTTPException, Depends, status
from modules.user.schema import UserUpdate, UserCreate
from sqlalchemy.orm import Session
from modules.authentication.controller import token_manager
from database_utili.database import get_session
from modules.authentication.models import User
from datetime import datetime
from fastapi.encoders import jsonable_encoder



#function to update the user from the database using its unique id
def update_user(
    id: str,
    user: UserUpdate,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_to_update = db.query(User).filter_by(id=id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User id not found"
        )
    if user_to_update.id != existing_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this user"
        )

    if user.full_name is not None:
        user_to_update.full_name = user.full_name
    else:
        user_to_update.full_name = existing_user.full_name

    if user.address is not None:
        user_to_update.address = user.address
    else:
        user_to_update.address = existing_user.address

    if user.weight is not None:
        user_to_update.weight = user.weight
    else:
        user_to_update.weight = existing_user.weight

    if user.height is not None:
        user_to_update.height = user.height
    else:
        user_to_update.height = existing_user.height

    if user.DOB is not None:
        user_to_update.DOB = user.DOB
    else:
        user_to_update.DOB = existing_user.DOB

    if user.phone_number is not None:
        user_to_update.phone_number = user.phone_number
    else:
        user_to_update.phone_number = existing_user.phone_number

    if user.dietary_preference is not None:
        user_to_update.dietary_preference = user.dietary_preference
    else:
        user_to_update.dietary_preference = existing_user.dietary_preference

    if user.fitness_goal is not None:
        user_to_update.fitness_goal = user.fitness_goal
    else:
        user_to_update.fitness_goal = existing_user.fitness_goal

    if user.medical_condition is not None:
        user_to_update.medical_condition = user.medical_condition
    else:
        user_to_update.medical_condition = existing_user.medical_condition

    user_to_update.date_updated = datetime.utcnow()

    # Commit the changes to the database
    db.commit()

    return {"message": "User updated successfully"}
   

#function to delete a user from the database using its unique id
def delete_user(
    id: str,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_to_delete = db.query(User).filter_by(id=id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User id not found"
        )
    if user_to_delete.id != existing_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this user"
        )
    
    db.delete(user_to_delete)
    db.commit()


#function to display the current user info
def view_user(current_user: str = Depends(token_manager), db: Session = Depends(get_session)):

    existing_user = db.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return jsonable_encoder(existing_user)
  
