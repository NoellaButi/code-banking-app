# BankLite — Flask Banking App 🏦🌙💖  
Minimal banking demo with **Flask + SQLAlchemy**, authentication, HTML views, and a JSON API.

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)
![DB](https://img.shields.io/badge/database-SQLite%20%2F%20Postgres-7957D5.svg)
![Tests](https://img.shields.io/badge/tests-pytest-6aa84f.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

✨ **Overview**  
BankLite is a teaching/demo app for a tiny banking backend. Users sign up, create **Checking/Savings** accounts, and perform **deposit, withdraw, and transfer** operations. Data persists via **SQLAlchemy** (SQLite locally, Postgres in prod). It includes **CSRF-protected HTML forms**, a small **JSON API**, and **pytest** tests.

🧩 **What it shows**
- Flask app factory + blueprints
- SQLAlchemy models & migrations (Flask-Migrate/Alembic)
- Flask-Login auth, CSRF protection
- Business logic with atomic transfers
- JSON serialization with Marshmallow
- Tests (pytest) and optional GitHub Actions CI

---

## 📁 Repository Layout
```bash
code-banking-app/
├─ app/
│  ├─ __init__.py           # app factory + blueprints
│  ├─ config.py             # config (DATABASE_URL / SQLITE fallback)
│  ├─ extensions.py         # db, migrate, login_manager, csrf
│  ├─ models.py             # User, Account, Transaction
│  ├─ services.py           # deposit, withdraw, transfer (atomic)
│  ├─ routes.py             # HTML pages (dashboard, forms)
│  ├─ api.py                # JSON API endpoints
│  ├─ schemas.py            # Marshmallow schemas
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ auth/{login,signup}.html
│  │  └─ transactions/{list,transfer,deposit,withdraw}.html
│  └─ static/style.css      # dark + pink theme
├─ migrations/              # Alembic (created after `flask db init`)
├─ tests/                   # pytest tests
├─ .env.example             # sample env (copy to .env)
├─ .gitignore
├─ requirements.txt
├─ wsgi.py                  # gunicorn entrypoint
└─ README.md
```

## 🚀 Quickstart (Local Dev)

Requirements: 
```bash
Python 3.11+, pip
```

Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

copy .env.example .env
$env:FLASK_APP = "app"
# (Flask 3.x) Optional: $env:FLASK_DEBUG = "1"

# Database (SQLite file: banklite.db)
flask db init           # first time only
flask db migrate -m "init"
flask db upgrade

flask run
# http://127.0.0.1:5000
```

macOS/Linux (bash/zsh)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
export FLASK_APP=app
# Optional: export FLASK_DEBUG=1

flask db init           # first time only
flask db migrate -m "init"
flask db upgrade

flask run
# http://127.0.0.1:5000
```

## 🧭 Demo Walkthrough

- Visit /auth/signup → create a user
- Log in at /auth/login
- Create accounts at /accounts/new (e.g., Checking with 100.00)
- Use /deposit, /withdraw, or /transfer
- View /transactions to see the ledger (transfer shows as debit+credit rows)

## 🔌 API (JSON)

Auth is cookie-based (log in via the form first). Example calls assume an authenticated session.

List accounts
```http
GET /api/accounts
```

Create account
```http
POST /api/accounts
Content-Type: application/json
{
  "name": "Checking",
  "type": "Checking",
  "opening": "100.00"
}
```

Deposit
```http
POST /api/transactions/deposit
Content-Type: application/json
{
  "account_id": 1,
  "amount": "25.00",
  "description": "Paycheck"
}
```

Withdraw
```http
POST /api/transactions/withdraw
Content-Type: application/json
{
  "account_id": 1,
  "amount": "10.00",
  "description": "ATM"
}
```

Transfer
```http
POST /api/transactions/transfer
Content-Type: application/json
{
  "src": 1,
  "dst": 2,
  "amount": "25.00",
  "description": "Move to savings"
}
```

## 🧪 Tests
```bash
pytest -q
# or with coverage:
pytest --cov=app --cov-report=term-missing
```

## ⚙️ Configuration
Set via environment or .env:
```ini
# .env (see .env.example)
FLASK_DEBUG=1
SECRET_KEY=change-me-in-prod

# Local default:
SQLALCHEMY_DATABASE_URI=sqlite:///banklite.db

# Production (Render/Railway/Heroku):
# DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
app/config.py prefers DATABASE_URL if present, otherwise falls back to SQLALCHEMY_DATABASE_URI, else sqlite:///banklite.db.
```

## 🚢 Deploy

- WSGI: gunicorn app.wsgi:app
- DB: set DATABASE_URL to Postgres
- Run migrations once on boot: flask db upgrade
- Set SECRET_KEY in the environment

Example Proc/Start (platform-dependent):
```css
gunicorn --workers 2 --timeout 120 app.wsgi:app
```

## 🧭 Notes & Pitfalls

- Use Decimal semantics for money (DB column is Numeric(12,2)).
- Transfers are atomic and recorded as two entries (debit+credit).
- Protect all POST forms with CSRF (<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">).
- Enforce ownership on every operation: only act on the current user’s accounts.
- On SQLite, row locks are limited; on Postgres we use SELECT ... FOR UPDATE when available.

## 🔮 Roadmap

- JWT for API clients
- Pagination/filters on transactions
- CSV export of statements
- Admin role
- Docker Compose (app + Postgres)

## 📜 License
MIT (see [LICENSE](LICENSE))

---
