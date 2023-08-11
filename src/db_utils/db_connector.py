from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_connect(database_url):

    # Create a PostgreSQL database engine and session
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal