from modules.user.controller import update_user, delete_user, view_user
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from database_utili.database import get_session
from modules.authentication.schema import UserCreate
from modules.user.schema import UserUpdate
from modules.authentication.controller import token_manager



user = APIRouter(prefix="/api/v1.0", tags=["User Management"])

#route to update the user profile
@user.put("/edit_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_current_user_profile(id:str, user:UserUpdate, 
                               current_user:str = Depends(token_manager),
                               db:Session = Depends(get_session)):
    
    return update_user(id, user, current_user, db)


#route to delete a user 
@user.delete("/delete_user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(id:str,
                              current_user:str = Depends(token_manager),
                               db:Session = Depends(get_session)):
    
    return delete_user(id, current_user, db)


#route to get a user details
@user.get("/view_user", status_code=status.HTTP_200_OK)
async def view_current_user(current_user:str = Depends(token_manager),
                              db:Session = Depends(get_session)):
    
    return view_user(current_user, db)