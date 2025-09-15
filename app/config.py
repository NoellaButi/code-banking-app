# config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    uri = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///banklite.db")

    # Normalize to SQLAlchemy 2 + psycopg3
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
    elif uri.startswith("postgresql://"):
        uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}