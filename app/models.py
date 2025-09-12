# models.py
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager

# --------------------
# User model
# --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    accounts = db.relationship("Account", backref = "owner", lazy = True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


# --------------------
# Account model
# --------------------
class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    type = db.Column(db.String(30), nullable = False)   # e.g., Checking/Savings
    balance = db.Column(db.Numeric(12, 2), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    transactions = db.relationship("Transaction", backref = "account", lazy = True)


# --------------------
# Transaction model
# --------------------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    kind = db.Column(db.String(20), nullable = False)   # deposit/withdraw/transfer
    amount = db.Column(db.Numeric(12, 2), nullable = False)
    description = db.Column(db.String(255))
    related_account_id = db.Column(db.Integer)      # for transfers
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    @staticmethod
    def as_decimal(value: float | str | Decimal) -> Decimal:
        """Ensure all amounts are stored as Decimals with 2 dp precision."""
        return Decimal(str(value)).quantize(Decimal("0.01"))