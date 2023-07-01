from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# POSTGRES_DB = os.environ.get('DB_NAME')
# POSTGRES_USER = os.environ.get('DB_USER')
# POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')
# POSTGRES_HOST = os.environ.get('DB_HOST')

# URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
URL = 'sqlite:///book_catelog.db'

# engine = create_engine(URL)
engine = create_engine(URL, connect_args={'check_same_thread':False})

SessinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessinLocal()
    try:
        yield db
    finally:
        db.close()