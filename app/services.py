# services.py (business logic: atomic operations)
from __future__ import annotations

from decimal import Decimal
from flask import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from .extensions import db

from .models import Account, Transaction

def _to_money(value: float | str | Decimal) -> Decimal:
    amt = Transaction.as_decimal(value)
    if amt <= Decimal("0.00"):
        abort(400, description = "Amount must be positive")
    return amt

def create_account(user_id: int, name: str, type_: str, opening_balance: float | str = 0) -> Account:
    opening = Transaction.as_decimal(opening_balance)
    acct = Account(user_id = user_id, name = name, type = type_, balance = opening)
    db.session.add(acct)
    db.session.commit()
    return acct

def deposit(account: Account, amount: float | str, description: str = "") -> Transaction:
    amt = _to_money(amount)
    account.balance += amt
    t = Transaction(
        account_id = account.id,
        kind = "deposit",
        amount = amt,
        description = description or "Deposit",
    )
    db.session.add(t)
    db.session.commit()
    return t

def withdraw(account: Account, amount: float | str, description: str = "") -> Transaction:
    amt = _to_money(amount)
    if account.balance < amt:
        abort(400, description = "Insufficient funds")
    account.balance -= amt
    t = Transaction(
        account_id = account.id,
        kind = "withdraw",
        amount = amt,
        description = description or "Withdraw",
    )
    db.session.add(t)
    db.session.commit()
    return t

def transfer(src: Account, dst: Account, amount: float | str, description: str = "") -> Transaction:
    # reuse your positive-amount helper if you have it
    amt = Transaction.as_decimal(amount)
    if amt <= Decimal("0.00"):
        abort(400, description="Amount must be positive")

    if src.id == dst.id:
        abort(400, description="Cannot transfer to the same account")

    try:
        # Safe inside or outside an existing transaction
        with db.session.begin_nested():
            # Lock rows when supported (no-op on SQLite)
            dialect = db.session.get_bind().dialect.name
            if dialect in {"postgresql", "mysql"}:
                db.session.execute(
                    select(Account)
                    .where(Account.id.in_([src.id, dst.id]))
                    .with_for_update()
                )

            # Reload fresh instances within this tx
            src_ref = db.session.get(Account, src.id)
            dst_ref = db.session.get(Account, dst.id)
            if src_ref is None or dst_ref is None:
                abort(404, description="Account not found")

            if src_ref.user_id != dst_ref.user_id:
                abort(403, description="Cross-user transfer not allowed")

            if src_ref.balance < amt:
                abort(400, description="Insufficient funds")

            # Apply updates
            src_ref.balance = src_ref.balance - amt
            dst_ref.balance = dst_ref.balance + amt

            # Ledger entries
            t1 = Transaction(
                account_id=src_ref.id,
                kind="transfer",
                amount=amt,
                description=description or f"To {dst_ref.id}",
                related_account_id=dst_ref.id,
            )
            t2 = Transaction(
                account_id=dst_ref.id,
                kind="deposit",
                amount=amt,
                description=f"From {src_ref.id}",
                related_account_id=src_ref.id,
            )
            db.session.add_all([t1, t2])

        # Commit the outer transaction (or the implicit one)
        db.session.commit()
        return t1

    except IntegrityError:
        db.session.rollback()
        abort(500, description="Transfer failed")