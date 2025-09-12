# config.py
import os

class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Prefer DATABASE_URL (Render/Railway/Heroku), else fallback, else local SQLite
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///banklite.db")
    )

    # Disable modification tracking overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False