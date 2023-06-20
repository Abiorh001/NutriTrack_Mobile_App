from pydantic import BaseModel
from datetime import date



#Table schema for Authentication
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    address: str
    weight: float
    height: float
    DOB: date
    phone_number: int
    dietary_preference: str
    fitness_goal: str
    medical_condition: str
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "password": "password123",
                "address": "123 Address, Los Angeles, USA",
                "weight": 70.5,
                "height": 175.0,
                "DOB": "1990-01-01",
                "phone_number": 1234567890,
                "dietary_preference": "Vegetarian",
                "fitness_goal": "Weight Loss",
                "medical_condition": "None"
            }
        }


class UserSignin(BaseModel):
    email: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "password123"
               
            }
        }
    


class UserUpdate(BaseModel):
    password: str
    class Config:
        schema_extra = {
            "example": {
                "password": "password123"
               
            }
        }

class ForgetPassword(BaseModel):
    email: str
    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
            }
        }
    

class ResetPassword(BaseModel):
    password:str
    class Config:
        schema_extra = {
            "example": {
                "password": "password123"  
            }
        }
