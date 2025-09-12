# config.py
import os

class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Database URI
    # Prefer DATABASE_URL (used by Render, Railway, Heroku, etc.)
    # Fallback to SQLALCHEMY_DATABASE_URI or local SQLite
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///banklite.db")
    )

    # Disable modification tracking overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False