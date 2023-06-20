from database_utili.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from modules.authentication.models import User, RevokedToken
from fastapi_jwt_auth import AuthJWT
from modules.authentication.schema import UserCreate, UserSignin, UserUpdate
from fastapi.encoders import jsonable_encoder



# Function to check if the JWT token has been revoked or not
async def is_token_revoked(jti: str, session: Session):
    revoked_token = session.query(RevokedToken).filter_by(id=jti).first()
    return revoked_token is not None

# Function to create token manager to use JWT token and confirm user login
async def token_manager(Authorize: AuthJWT = Depends(), session: Session = Depends(get_session)):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()["jti"]

        if await is_token_revoked(jti, session):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        current_user = Authorize.get_jwt_subject()
        return current_user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing token")


# function to create a new user
def new_user(user: UserCreate, db: Session = Depends(get_session)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=generate_password_hash(user.password, method="scrypt"),
        address=user.address,
        weight=user.weight,
        height=user.height,
        DOB=user.DOB,
        phone_number=user.phone_number,
        dietary_preference=user.dietary_preference,
        fitness_goal=user.fitness_goal,
        medical_condition=user.medical_condition
    )

    # add new_user to database
    db.add(new_user)

    # commit the change to database to take effect
    db.commit()

    # refresh database
    db.refresh(new_user)

    return jsonable_encoder(new_user), {"message": "New user created"}
