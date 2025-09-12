# test_models.py
from decimal import Decimal

from app.extensions import db
from app.models import User, Account


def test_user_password_hash(app):
    u = User(email = "a@b.com")
    u.set_password("secret")
    db.session.add(u)
    db.session.commit()

    # Hash shouldn't equal the raw password
    assert u.password_hash != "secret"
    assert u.check_password("secret") is True
    assert u.check_password("wrong") is False

def test_create_account(app):
    # Create a user
    u = User(email = "c@d.com")
    u.set_password("x")
    db.session.add(u)
    db.session.commit()

    # Create account for that user
    a = Account(user_id = u.id, name = "Main", type = "Checking")
    db.session.add(a)
    db.session.commit()

    # Got an id, linked to user, default balance is zero
    assert a.id is not None
    assert a.owner.id == u.id
    assert a.balance == Decimal("0")

    # Relationship visible from user side too
    db.session.refresh(u)
    assert len(u.accounts) == 1
    assert u.accounts[0].id == a.id