# routes.py (HTML views)
from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .extensions import db
from .models import Account, Transaction
from .services import create_account, deposit, withdraw, transfer

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return render_template("index.html", accounts = accounts)

@bp.route("/accounts/new", methods = ["GET", "POST"])
@login_required
def new_account():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        type_ = (request.form.get("type") or "Checking").strip()
        opening = request.form.get("opening", "0")

        if not name:
            flash("Account name is required.", "error")
            return redirect(url_for("main.new_account"))

        create_account(current_user.id, name, type_, opening)
        flash("Account created.", "success")
        return redirect(url_for("main.index"))

    return render_template("accounts/new.html")

@bp.route("/transactions", methods = ["GET"])
@login_required
def transactions_list():
    # All transactions across the user's accounts, newest first
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    ids = [a.id for a in accounts]
    tx = (
        Transaction.query.filter(Transaction.account_id.in_(ids))
        .order_by(Transaction.created_at.desc())
        .all()
    )
    return render_template("transactions/list.html", tx = tx, accounts = accounts)

@bp.route("/transfer", methods = ["GET", "POST"])
@login_required
def transfer_view():
    accounts = Account.query.filter_by(user_id = current_user.id).all()

    if request.method == "POST":
        try:
            src_id = int(request.form["src"])
            dst_id = int(request.form["dst"])
            amount = request.form["amount"]
        except (KeyError, ValueError):
            flash("Please select valid accounts and amount.", "error")
            return redirect(url_for("main.transactions_view"))

        src = Account.query.get_or_404(src_id)
        dst = Account.query.get_or_404(dst_id)

        # Ensure both accounts belong to the logged-in user
        if src.user_id != current_user.id or dst.user_id != current_user.id:
            flash("You can only between your own accounts.", "error")
            return redirect(url_for("main.transactions_view"))

        if src.id == dst.id:
            flash("Choose two different accounts.", "error")
            return redirect(url_for("main.transactions_view"))

        # Perform atomic transfer (services handles validation/atomicity)
        transfer(src, dst, amount, description = "User transfer")

        flash("Transfer complete.", "success")
        return  redirect(url_for("main.transactions_list"))

    return render_template("transactions/transfer.html", accounts = accounts)

@bp.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit_view():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        account_id = int(request.form["account_id"])
        amount = request.form["amount"]
        description = request.form.get("description", "")
        account = Account.query.get_or_404(account_id)
        if account.user_id != current_user.id:
            flash("You can only deposit to your own account", "error")
            return redirect(url_for("main.deposit_view"))
        t = deposit(account, amount, description=description)
        flash(f"Deposited {amount} to {account.name}", "success")
        return redirect(url_for("main.transactions_list"))
    return render_template("transactions/deposit.html", accounts=accounts)


@bp.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw_view():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        account_id = int(request.form["account_id"])
        amount = request.form["amount"]
        description = request.form.get("description", "")
        account = Account.query.get_or_404(account_id)
        if account.user_id != current_user.id:
            flash("You can only withdraw from your own account", "error")
            return redirect(url_for("main.withdraw_view"))
        try:
            t = withdraw(account, amount, description=description)
        except Exception as e:
            # services.withdraw already aborts on insufficient funds; we catch generic to surface message
            flash(getattr(e, "description", "Withdraw failed"), "error")
            return redirect(url_for("main.withdraw_view"))
        flash(f"Withdrew {amount} from {account.name}", "success")
        return redirect(url_for("main.transactions_list"))
    return render_template("transactions/withdraw.html", accounts=accounts)