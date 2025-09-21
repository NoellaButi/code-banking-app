# __init__.py
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, login_manager, csrf, migrate

def create_app(config_object: type[Config] = Config) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_object)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # blueprints
    from .auth import bp as auth_bp
    from .routes import bp as main_bp
    from .api import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # --- make sure models are imported so migrations can detect them ---
    from . import models as models

    return app
