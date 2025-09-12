# conftest.py
import pytest
from app import create_app
from app.config import Config
from app.extensions import db

@pytest.fixture()
def app():
    class TestConfig(Config):
        TESTING = True
        SECRET_KEY = "test"
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_CSRF_ENABLED = False

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


# ------------ Convenience fixtures for common test setup ------------

@pytest.fixture()
def user(app):
    from app.models import User
    u = User(email = "text@example.com")
    u.set_password("password123")
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture()
def auth_client(client, user):
    # Logs in via the HTML from endpoints (CSRF disabled in TestConfig)
    client.post("/auth/login", data = {"email": user.email, "password": "password123"}, follow_redirects = True)
    return client

@pytest.fixture()
def accounts(app, user):
    """Create two accounts for transfers."""
    from app.services import create_account
    a1 = create_account(user.id, "Checking", "Checking", 100)
    a2 = create_account(user.id, "Savings", "Savings", 50)
    return a1, a2