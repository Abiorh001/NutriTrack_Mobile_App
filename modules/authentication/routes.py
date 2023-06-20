from modules.authentication.controller import new_user, email_confirmation ,sign_in, sign_out, forget_password, reset_password
from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from database_utili.database import get_session
from modules.authentication.schema import UserCreate, UserSignin, ForgetPassword, ResetPassword
from fastapi_jwt_auth import AuthJWT



auth = APIRouter(prefix="/api/v1.0", tags=["Authentication"])

#route to sign up a new user
@auth.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def register_new_user(user:UserCreate, request:Request, db:Session = Depends(get_session)):

    return new_user(user, request, db)

# route to confirm user email address
@auth.post("/email_confirmation", status_code=status.HTTP_200_OK)
async def new_user_email_confirmation(email_confirmation_token:str, db:Session = Depends(get_session)):

    return email_confirmation(email_confirmation_token, db)


 # Route to login an existing user
@auth.post("/sign_in", status_code=status.HTTP_200_OK)
async def login_existing_user(user: UserSignin, Authorize: AuthJWT = Depends(), 
                 db: Session = Depends(get_session)):
    return sign_in(user, Authorize, db)

# Route to log out a user
@auth.post("/sign_out")
async def logout_existing_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_session)):
    return sign_out(Authorize, db)

# route to reset existing user password
@auth.post("/forget_password", status_code=status.HTTP_202_ACCEPTED)
async def existing_user_forget_password(user:ForgetPassword, request: Request, 
                                        db:Session = Depends(get_session)):
    
    return forget_password(user, request, db)


# route to change old password to new password
@auth.post("/reset_password", status_code=status.HTTP_202_ACCEPTED)
async def existing_user_reset_password(user:ResetPassword, reset_token:str, 
                                        db:Session = Depends(get_session)):
    return reset_password(user, reset_token, db)