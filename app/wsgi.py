# wsgi.py
from __future__ import annotations
import os
from app import create_app
from flask_migrate import upgrade

app = create_app()

# --- Run migrations automatically on startup (prod only) ---
RUN_DB_MIGRATIONS = os.getenv("RUN_DB_MIGRATIONS", "1")  # default on
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI", "")

if RUN_DB_MIGRATIONS == "1" and db_uri.startswith(("postgresql+psycopg://", "postgresql+psycopg:")):
    with app.app_context():
        try:
            upgrade()
            print("Database upgraded on startup")
        except Exception as e:
            print(f"Could not run migrations: {e}")

if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_RUN_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
