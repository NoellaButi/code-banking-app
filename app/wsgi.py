# wsgi.py
import os
from app import create_app
from flask_migrate import upgrade

app = create_app()

RUN_DB_MIGRATIONS = os.getenv("RUN_DB_MIGRATIONS", "1")
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI", "")

if RUN_DB_MIGRATIONS == "1" and db_uri.startswith(("postgresql+psycopg://", "postgresql+psycopg:")):
    with app.app_context():
        try:
            upgrade()
            print("Database upgraded on startup")
        except Exception as e:
            print(f"Could not run migrations: {e}")
