from database_utili.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from werkzeug.security import generate_password_hash, check_password_hash
from modules.authentication.models import User, RevokedToken
from fastapi_jwt_auth import AuthJWT
from modules.authentication.schema import UserCreate, UserSignin, UserUpdate, ForgetPassword, ResetPassword
from fastapi.encoders import jsonable_encoder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets




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
def new_user(user: UserCreate, request:Request, db: Session = Depends(get_session)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
   
    # generating email confirmation token
    email_confirmation_token = secrets.token_hex(16)
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
        medical_condition=user.medical_condition,
        email_confirmation_token=email_confirmation_token
    )

    # add new_user to database
    db.add(new_user)


    # commit the change to database to take effect
    db.commit()

    # SMTP server details
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  
    smtp_username = 'abiolaadedayo1993@gmail.com'
    smtp_password = 'etkazqurxvtqouak'  

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = "abiolaadedayo1993@gmail.com"
    msg["To"] = user.email
    msg["Subject"] = "Confirm Email Address"
    # Add the schedule data to the email body

    # Construct the reset URL
    email_confirmation_url = str(request.base_url) + "email_confirmation?token=" + email_confirmation_token

    # Add the reset URL and token to the email body
    body = f"email address confirmation:\n\nPlease click the link below to confirm your email:\n\n{email_confirmation_url}"
    msg.attach(MIMEText(body, "plain"))


    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        # Login to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.send_message(msg)
        # Close the SMTP server connection
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"message": "Failed to send email", "error": str(e)}

    

#function for new user email confirmation
def email_confirmation(email_confirmation_token:str, db: Session = Depends(get_session)):

    existing_user = db.query(User).filter_by(email_confirmation_token=email_confirmation_token).first()
    if existing_user:
        existing_user.email_confirmation_token = None
        db.commit()
        return {"message":"email address confirmed succesfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email confirmation token is invalid or missing")



#function to login existing user
def sign_in(user: UserSignin, Authorize: AuthJWT = Depends(), 
            db: Session = Depends(get_session)):
    
    
    existing_user = db.query(User).filter_by(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email does not exist")
    
    if existing_user.email_confirmation_token is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User email address not confirmed")

    if not check_password_hash(existing_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")

    
    #set access token
    access_token = Authorize.create_access_token(subject=user.email)

    return {"access_token": access_token}

#function to log out user
def sign_out(Authorize: AuthJWT = Depends(), db: Session = Depends(get_session)):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()["jti"]

        revoked_token = RevokedToken(id=jti)
        db.add(revoked_token)
        db.commit()

        return {"message": "Logged out successfully"}

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    


#function for forget password
def forget_password(user:ForgetPassword, request:Request, db:Session = Depends(get_session)):

    existing_user = db.query(User).filter_by(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
 
    
    existing_user.reset_token = secrets.token_hex(16)

    #update the reset_token
    db.commit()

    # SMTP server details
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  
    smtp_username = 'abiolaadedayo1993@gmail.com'
    smtp_password = 'etkazqurxvtqouak'  

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = "abiolaadedayo1993@gmail.com"
    msg["To"] = user.email
    msg["Subject"] = "Reset Password"
    # Add the schedule data to the email body

    # Construct the reset URL
    reset_url = str(request.base_url) + "reset_password?reset_token=" + existing_user.reset_token

    # Add the reset URL and token to the email body
    body = f"Reset Password confirmation:\n\nPlease click the link below to reset your password:\n\n{reset_url}"
    msg.attach(MIMEText(body, "plain"))


    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        # Login to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.send_message(msg)
        # Close the SMTP server connection
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"message": "Failed to send email", "error": str(e)}
    



#function to reset pasword
def reset_password(user:ResetPassword, reset_token:str, db: Session = Depends(get_session)):

    existing_user = db.query(User).filter_by(reset_token=reset_token).first()
    if existing_user:
        existing_user.password = generate_password_hash(user.password, method="scrypt")
        existing_user.reset_token = None
        db.commit()

        return {"message":"password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="reset token is invalid or missing")


   




