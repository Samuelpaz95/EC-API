import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

database_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USER"),
    os.getenv("DB_PASS"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME")
)

engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        print("Closing DB connection")
        db.close()
