from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


def db_connect(drivername, username, host, database):

    database_url = URL.create(
        drivername=drivername,
        username=username,
        host=host,
        database=database
    )
    # Create a PostgreSQL database engine and session
    engine = create_engine(database_url)
    connection = engine.connect()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()