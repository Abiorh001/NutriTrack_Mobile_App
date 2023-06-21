from fastapi import APIRouter, Depends, status, Query
from modules.food_logging.schema import FoodLoggingCreate
from sqlalchemy.orm import Session
from modules.authentication.controller import token_manager
from database_utili.database import get_session
from modules.food_logging.controller import (new_foodlogging,food_to_update, delete_food_log, 
                                             all_food_logs, view_food_log, all_food_logs_between_date,
                                             all_food_logs_by_date, total_food_logs, total_food_logs_by_duration,
                                             food_logs_filter_search)
from datetime import date


food_log = APIRouter(prefix="/api/v1.0", tags=["Food Logging"])



# Route to create a new food log
@food_log.post("/new_food_log", status_code=status.HTTP_201_CREATED)
async def new_food_log(
    food: FoodLoggingCreate,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    return new_foodlogging(food, current_user, db)



# Route to update an existing food log
@food_log.put("/edit_food_log/{id}", status_code=status.HTTP_202_ACCEPTED)
async def food_log_to_be_updated(
    id:str,
    food: FoodLoggingCreate,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    return food_to_update(id, food, current_user, db)

# Route to delete an existing  food log
@food_log.delete("/delete_food_log/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def food_log_to_be_deleted(
    id:str,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session)
):
    return delete_food_log(id, current_user, db)


# route to get all food logs
@food_log.get("/all_food_logs", status_code=status.HTTP_200_OK)
async def list_all_food_logs(
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    return all_food_logs(current_user, db, page, page_size)


# route to view a food log using it's unique id
@food_log.get("/food_log/{id}", status_code=status.HTTP_200_OK)
async def view_food_log_by_its_id(
    id:str,
    current_user:str = Depends(token_manager),
    db:Session = Depends(get_session)
):
    return view_food_log(id, current_user, db)


# route to get all food logs between start and end date
@food_log.get("/all_food_logs_between_dates", status_code=status.HTTP_200_OK)
async def list_all_food_logs_between_date_created(
    start_date:date,
    end_date:date,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    return all_food_logs_between_date(start_date, end_date, current_user, db, page, page_size)


# route to list all food logs by it's date created
@food_log.get("/all_food_logs_by_date", status_code=status.HTTP_200_OK)
async def list_all_food_logs_by_date_created(
    date:date,
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    
    return all_food_logs_by_date(date, current_user, db, page, page_size)


#route to get the summary of food logs daily
@food_log.get("/all_food_logs_summary", status_code=status.HTTP_200_OK)
async def summary_of_daily_food_logs(
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session) 
):
    return total_food_logs(current_user, db)


#route to get the summary of food logs by weekly or monthly
@food_log.get("/all_food_logs_summary_by_duration", status_code=status.HTTP_200_OK)
async def summary_of_food_logs_by_weekly_or_monthly(
    duration:str = Query(..., description="Duration of summary (week/month)"),
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session) 
):
    return total_food_logs_by_duration(duration, current_user, db)


# route to filter and search food logs by text input for the food
@food_log.get("/all_food_logs_filter_and_search", status_code=status.HTTP_200_OK)
async def all_food_logs_through_filter_and_search(
    food_name: str = Query(None, description="Search query string to filter food logs"),
    current_user: str = Depends(token_manager),
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):

    return food_logs_filter_search(food_name, current_user,
                                                   db, page, page_size)
