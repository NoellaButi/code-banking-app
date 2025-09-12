# api.py (JSON API)
from __future__ import annotations

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from marshmallow import ValidationError

from .extensions import db, csrf
from .models import Account, Transaction
from .services import create_account, deposit, withdraw, transfer
from .schemas import (
account_schema,
accounts_schema,
account_create_schema,
transaction_schema,
transactions_schema,
transaction_create_schema,
)

bp = Blueprint("api", __name__, url_prefix = "/api")
csrf.exempt(bp)     # JSON API: skip CSRF tokens on POST/PUT/PATCH/DELETE

# ------------ Helpers ------------
@bp.errorhandler(ValidationError)
def _handle_validation(err: ValidationError):
    return jsonify({"error": "validation error", "messages": err.messages})


def _ensure_owner(account: Account) -> None:
    if account.user_id != current_user.id:
        abort(403)


# ------------ Accounts ------------
@bp.get("/accounts")
@login_required
def list_accounts():
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return jsonify(accounts_schema.dump(accounts))

@bp.post("/accounts")
@login_required
def create_account_api():
    payload = account_create_schema.load(request.get_json() or {})
    acct = create_account(
        current_user.id,
        payload["name"],
        payload["type"],
        payload.get("opening", 0),
    )
    return jsonify(account_schema.dump(acct)), 201


# ------------ Transactions ------------
@bp.get("/transactions")
@login_required
def list_transactions():
    ids = [a.id for a in Account.query.filter_by(user_id = current_user.id).all()]
    tx = (
        Transaction.query.filter(Transaction.account_id.in_(ids))
        .order_by(Transaction.created_at.desc())
        .all()
    )
    return jsonify(transactions_schema.dump(tx))

@bp.post("/transactions")
@login_required
def deposit_api():
    data = request.get_json() or {}
    payload = transaction_create_schema.load(
        {
            "account_id": data.get("account_id"),
            "amount": data.get("amount"),
            "description": data.get("description", ""),
            "kind": "deposit",
        }
    )

    account = Account.query.get_or_404(payload["account_id"])
    _ensure_owner(account)

    t = deposit(account, payload["amount"], description = payload.get("description", ""))
    return jsonify(transaction_schema.dump(t)), 201

@bp.post("/transactions/withdraw")
@login_required
def withdraw_api():
    data = request.get_json() or {}
    payload = transaction_create_schema.load(
        {
            "account_id": data.get("account_id"),
            "amount": data.get("amount"),
            "description": data.get("description", ""),
            "kind": "withdraw",
        }
    )

    account = Account.query.get_or_404(payload["account_id"])
    _ensure_owner(account)

    t = withdraw(account, payload["amount"], description = payload.get("description", ""))
    return jsonify(transaction_schema.dump(t)), 201

@bp.post("/transactions/transfer")
@login_required
def transfer_api():
    data = request.get_json() or {}
    payload = transaction_create_schema.load(
        {
            "account_id": data.get("src"),
            "related_account_id": data.get("dst"),
            "amount": data.get("amount"),
            "description": data.get("description", ""),
            "kind": "transfer",
        }
    )

    src = Account.query.get_or_404(payload["account_id"])
    dst = Account.query.get_or_404(payload["related_account_id"])
    _ensure_owner(src)
    _ensure_owner(dst)

    t = transfer(src, dst, payload["amount"], description = payload.get("description", ""))
    return jsonify(transaction_schema.dump(t)), 201