from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<IP_ADDRESS>/<hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    print("DB Connection called")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg2.connect(host='172.17.0.3', database='fastapi', user='postgres', password='adminadmin', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was successful!")
# except Exception as error:
#     print("Database connection failed!")
#     print("Error:" + error)