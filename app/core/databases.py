from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session():
    """Context manager to handle database session lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()