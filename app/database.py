import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# En local/tests : SQLite. Dans Docker : PostgreSQL via la variable d'env.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
