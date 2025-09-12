# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

# --- Flask Extensions ---
db = SQLAlchemy()                   # ORM
login_manager = LoginManager()      # User session management
csrf = CSRFProtect()                # CSRF protection for forms/APIs
migrate = Migrate()                 # Database migrations (Flask-Migrate + Alembic)

# Configure login_manager
# This tells Flask_Login which endpoint handles login
# Example: @auth_bp.route("/login")
login_manager.login_view = "auth.login"