from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the database URI from the environment variables
sqlalchemy_database_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

# Define database engine with connection pooling and other optimizations
engine = create_engine(
    sqlalchemy_database_uri,
    pool_size=10,  # Set an appropriate pool size based on your application's needs
    max_overflow=20,  # Set the max overflow to handle occasional spikes in traffic
    pool_pre_ping=True,  # Enable pool pre-ping to detect and refresh stale connections
    echo=True  # Disable echoing SQL statements for production
)

# Create metadata and base class
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Create session factory
Session = sessionmaker(bind=engine)


# Creating a session factory for the database
def get_session():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
