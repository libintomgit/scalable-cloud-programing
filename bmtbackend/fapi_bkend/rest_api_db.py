from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

### python3 -m pip install sqlalchemy
# SQLALCHEMY_DAATABASE_URL = "sqlite:///./todos.db"

# engine = create_engine(
#     SQLALCHEMY_DAATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

## python3 -m pip install psycopg2-binary
SQLALCHEMY_DAATABASE_URL = "postgresql://libintom:password123@localhost/bmt_bkend_db_1"
# SQLALCHEMY_DAATABASE_URL = "postgresql://libintom:password123@ec2-100-25-221-164.compute-1.amazonaws.com/bmtdb1"

engine = create_engine(SQLALCHEMY_DAATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

### python3 -m pip install pymysql

# SQLALCHEMY_DAATABASE_URL = "mysql+pymysql://root:popopo123@127.0.0.1:3306/todo_app_db1"

# engine = create_engine(SQLALCHEMY_DAATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()