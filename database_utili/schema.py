from pydantic import BaseSettings
from datetime import timedelta



#creating table schema for database configuration
class Settings(BaseSettings):
    authjwt_secret_key: str = '47dhhd00fkfjhhr@ww'
    authjwt_access_token_expires: timedelta = timedelta(hours=120)