from fastapi import FastAPI
from modules.authentication.routes import auth
from fastapi_jwt_auth import AuthJWT
from database_utili.schema import Settings
from database_utili.database import metadata, engine






app = FastAPI(version=1.0, 
              description="NutriTrack is a comprehensive nutrition mobile application that empowers you to achieve a healthier lifestyle. With our user-friendly platform,\
                  you can effortlessly track your daily calorie intake, set personalized nutrition goals, and make informed food choices. We provide expert nutrition tips\
                      and evidence-based information to optimize your health and well-being. Take control of your diet and embark on a journey towards better nutrition with NutriTrack.",
              title="NutriTrack Mobile App")

#load jwt secret key from schema
@AuthJWT.load_config
def get_config():
    return Settings()

# Create the database tables if they don't exist
metadata.create_all(engine)

#adding our routes
app.include_router(auth)



