from fastapi import HTTPException, Depends, status, Query
from modules.food_logging.models import FoodLogging
from modules.food_logging.schema import FoodLoggingCreate
from sqlalchemy.orm import Session
from modules.authentication.controller import token_manager
from database_utili.database import get_session
import requests
from modules.authentication.models import User
from datetime import datetime, date, timedelta
from sqlalchemy import func





# Function to create a new food log
def new_foodlogging(
    food: FoodLoggingCreate,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

    headers = {
        'Content-Type': 'application/json',
        'x-app-id': '084477a5',
        'x-app-key': 'd4e9fb17c214d065fa070d51d9d71d4d'
    }

    payload = {
        'query': food.food_name
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()

        foods = data['foods']
        for food_data in foods:
            new_food = FoodLogging(
                food_name=food_data['food_name'],
                brand_name=food_data['brand_name'],
                serving_qty=food_data['serving_qty'],
                serving_unit=food_data['serving_unit'],
                serving_weight_grams=food_data['serving_weight_grams'],
                calories=food_data['nf_calories'],
                total_fat=food_data['nf_total_fat'],
                saturated_fat=food_data['nf_saturated_fat'],
                cholesterol=food_data['nf_cholesterol'],
                sodium=food_data['nf_sodium'],
                total_carbohydrate=food_data['nf_total_carbohydrate'],
                dietary_fiber=food_data['nf_dietary_fiber'],
                sugars=food_data['nf_sugars'],
                protein=food_data['nf_protein'],
                potassium=food_data['nf_potassium'],
                p=food_data['nf_p'],
                is_raw_food=food_data['metadata']['is_raw_food'],
                user_id=existing_user.id
            )
            db.add(new_food)

        # Commit the changes and close the session
        db.commit()
        return {"message":"New Food Log Created"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch food information"
        )


 # function to update a food log from the database using its unique id
def food_to_update(
    id: str,
    food: FoodLoggingCreate,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    food_to_update = db.query(FoodLogging).filter_by(id=id).first()

    if not food_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food log not found"
        )
    if food_to_update.user_id != existing_user.id:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have permission to update this food log"
        )

    food_to_update.food_name = food.food_name

    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': '084477a5',
        'x-app-key': 'd4e9fb17c214d065fa070d51d9d71d4d'
    }
    payload = {
        'query': food_to_update.food_name
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        foods = data.get('foods', [])

        if not foods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch food information"
            )
        

        food_data = foods[0]  # Assuming only one food is returned

        food_to_update.food_name = food_data.get('food_name')
        food_to_update.brand_name = food_data.get('brand_name')
        food_to_update.serving_qty = food_data.get('serving_qty')
        food_to_update.serving_unit = food_data.get('serving_unit')
        food_to_update.serving_weight_grams = food_data.get('serving_weight_grams')
        food_to_update.calories = food_data.get('nf_calories')
        food_to_update.total_fat = food_data.get('nf_total_fat')
        food_to_update.saturated_fat = food_data.get('nf_saturated_fat')
        food_to_update.cholesterol = food_data.get('nf_cholesterol')
        food_to_update.sodium = food_data.get('nf_sodium')
        food_to_update.total_carbohydrate = food_data.get('nf_total_carbohydrate')
        food_to_update.dietary_fiber = food_data.get('nf_dietary_fiber')
        food_to_update.sugars = food_data.get('nf_sugars')
        food_to_update.protein = food_data.get('nf_protein')
        food_to_update.potassium = food_data.get('nf_potassium')
        food_to_update.p = food_data.get('nf_p')
        food_to_update.is_raw_food = food_data.get('metadata', {}).get('is_raw_food')
        food_to_update.date_updated = datetime.utcnow()

      

        db.commit()
        return {"message": "Food Log Has Been Updated Successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch food information"
        )
    
# function to delete a food log from the database using its unique id
def delete_food_log(
    id: str,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    food_to_delete = db.query(FoodLogging).filter_by(id=id).first()

    if not food_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food log not found"
        )
    
    if food_to_delete.user_id != existing_user.id:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have permission to delete this food log"
        )
    
    db.delete(food_to_delete)
    db.commit()


# function to get all food logs 
def all_food_logs(
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

   

    total_food_logs = db.query(FoodLogging).filter_by(user_id=existing_user.id).count()

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Query the entries with pagination
    food_log = (
        db.query(FoodLogging)
        .filter_by(user_id=existing_user.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
            "total food logs": total_food_logs,
            "page": page,
            "page_size": page_size,
            "entries": food_log,
        }

# function to display a food log using it's unique address
def view_food_log(
        id:str,
        current_user:str = Depends(token_manager),
        db:Session = Depends(get_session)
):
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    
    food_log = db.query(FoodLogging).filter_by(id=id).first()
    if not food_log:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food log not found"
            )
    if food_log.user_id != existing_user.id:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have permission to view this food log"
        )
    
    return food_log

# Retrieves food logs within a specified date range.
def all_food_logs_between_date(
    start_date:date,
    end_date:date,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

   

    total_food_logs = db.query(FoodLogging).filter_by(user_id=existing_user.id).count()

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Query the entries with pagination
    food_log = (
        db.query(FoodLogging)
        .filter(FoodLogging.user_id == existing_user.id)
        .filter(FoodLogging.date.between(start_date, end_date))
        .offset(offset)
        .limit(page_size)
        .all()
    )


    return {
            "total food logs": total_food_logs,
            "page": page,
            "page_size": page_size,
            "entries": food_log,
        }

# function to Retrieves food logs for a specific date.
def all_food_logs_by_date(
    date:date,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

   

    total_food_logs = db.query(FoodLogging).filter_by(user_id=existing_user.id).count()

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Query the entries with pagination
    food_log = (
        db.query(FoodLogging)
        .filter(FoodLogging.user_id == existing_user.id)
        .filter(FoodLogging.date == date)
        .offset(offset)
        .limit(page_size)
        .all()
    )


    return {
            "total food logs": total_food_logs,
            "page": page,
            "page_size": page_size,
            "food logs": food_log,
        }


# function to give summary of the food log daily
def total_food_logs(
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session) 
):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


    today = date.today()
    total_calories = (
        db.query(func.sum(FoodLogging.calories))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    total_serving_weight_grams = (
        db.query(func.sum(FoodLogging.serving_weight_grams))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )

    total_fat = (
        db.query(func.sum(FoodLogging.total_fat))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_saturated_fat = (
        db.query(func.sum(FoodLogging.saturated_fat))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_cholesterol = (
        db.query(func.sum(FoodLogging.cholesterol))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_sodium = (
        db.query(func.sum(FoodLogging.sodium))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_carbohydrate = (
        db.query(func.sum(FoodLogging.total_carbohydrate))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_dietary_fiber = (
        db.query(func.sum(FoodLogging.dietary_fiber))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_sugars = (
        db.query(func.sum(FoodLogging.sugars))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_protein = (
        db.query(func.sum(FoodLogging.protein))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_potassium = (
        db.query(func.sum(FoodLogging.potassium))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_p = (
        db.query(func.sum(FoodLogging.p))
        .filter(func.DATE(FoodLogging.date) == today, FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    return {
        "message":"total calories, macronutrients, and other metrics for daily food logs.",
        "total_calories": total_calories,
        "total_serving_weight_grams": total_serving_weight_grams,
        "total_fat": total_fat,
        "total_saturated_fat": total_saturated_fat,
        "total_cholesterol": total_cholesterol,
        "total_sodium": total_sodium,
        "total_carbohydrate": total_carbohydrate,
        "total_dietary_fiber": total_dietary_fiber,
        "total_sugars": total_sugars,
        "total_protein": total_protein,
        "total_potassium": total_potassium,
        "total_p": total_p
    }


# function to give summary of the food log by weekly or montly 
def total_food_logs_by_duration(
    duration: str = Query(..., description="Duration of summary (week/month)"),
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session) 
):
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    today = date.today()
    start_date = None
    end_date = None
    
    if duration == "week":
        start_date = today - timedelta(days=7)
        end_date = today
    elif duration == "month":
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid duration. Valid durations are 'week' and 'month'."
        )
    
    total_calories = (
        db.query(func.sum(FoodLogging.calories))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_serving_weight_grams = (
        db.query(func.sum(FoodLogging.serving_weight_grams))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_fat = (
        db.query(func.sum(FoodLogging.total_fat))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_saturated_fat = (
        db.query(func.sum(FoodLogging.saturated_fat))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_cholesterol = (
        db.query(func.sum(FoodLogging.cholesterol))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_sodium = (
        db.query(func.sum(FoodLogging.sodium))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_carbohydrate = (
        db.query(func.sum(FoodLogging.total_carbohydrate))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_dietary_fiber = (
        db.query(func.sum(FoodLogging.dietary_fiber))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_sugars = (
        db.query(func.sum(FoodLogging.sugars))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_protein = (
        db.query(func.sum(FoodLogging.protein))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_potassium = (
        db.query(func.sum(FoodLogging.potassium))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    total_p = (
        db.query(func.sum(FoodLogging.p))
        .filter(FoodLogging.date.between(start_date, end_date), FoodLogging.user_id == existing_user.id)
        .scalar()
    )
    
    return {
        "message":f"total calories, macronutrients, and other metrics per {duration} for food logs.",
        "duration": duration,
        "start_date": start_date,
        "end_date": end_date,
        "total_calories": total_calories,
        "total_serving_weight_grams": total_serving_weight_grams,
        "total_fat": total_fat,
        "total_saturated_fat": total_saturated_fat,
        "total_cholesterol": total_cholesterol,
        "total_sodium": total_sodium,
        "total_carbohydrate": total_carbohydrate,
        "total_dietary_fiber": total_dietary_fiber,
        "total_sugars": total_sugars,
        "total_protein": total_protein,
        "total_potassium": total_potassium,
        "total_p": total_p
    }


# function to filter and search food logs by text input for the food
def food_logs_filter_search(
    food_name: str = Query(None, description="Search query string to filter entries"),
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    
    existing_user = db.query(User).filter_by(email=current_user).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Create a query to filter food logs based on the search query
    food_log_query = db.query(FoodLogging).filter(FoodLogging.user_id == existing_user.id)
    if food_name:
        food_log_query = food_log_query.filter(FoodLogging.food_name.ilike(f"%{food_name}%"))

    total_food_logs = food_log_query.count()

    offset = (page - 1) * page_size

    # Query the filtered entries with pagination
    food_logs = food_log_query.offset(offset).limit(page_size).all()

    return {
        "total_food_logs": total_food_logs,
        "page": page,
        "page_size": page_size,
        "food_logs": food_logs
    }
