from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from decouple import config

# POSTGRES_DB = config('DB_NAME')
# POSTGRES_USER = config('DB_USER')
# POSTGRES_PASSWORD = config('DB_PASSWORD')
# POSTGRES_HOST = config('DB_HOST')

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