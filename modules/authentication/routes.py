from modules.authentication.controller import new_user
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database_utili.database import get_session
from modules.authentication.schema import UserCreate



auth = APIRouter(prefix="/api/v1.0", tags=["Authentication"])

#route to sign up a new user
@auth.post("/signup")
async def signup(user:UserCreate, db:Session = Depends(get_session)):

    return new_user(user, db)