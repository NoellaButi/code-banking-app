# auth.py (signup/login/logout)
from __future__ import annotations

from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from .extensions import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def _is_safe_url(target: str) -> bool:
    if not target:
        return False
    ref = urlparse(request.host_url)
    test = urlparse(urljoin(request.host_url, target))
    return (test.scheme in ("http", "https")) and (ref.netloc == test.netloc)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("auth.signup"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("auth.signup"))

        u = User(email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        remember = bool(request.form.get("remember"))

        u = User.query.filter_by(email=email).first()
        if not u or not u.check_password(password):
            flash("Invalid credentials.", "error")
            return redirect(url_for("auth.login"))

        login_user(u, remember=remember)

        next_url = request.args.get("next") or request.form.get("next")
        if next_url and _is_safe_url(next_url):
            return redirect(next_url)
        return redirect(url_for("main.index"))

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("main.index"))