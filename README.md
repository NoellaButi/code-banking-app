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
│  ├─ wsgi.py               # gunicorn entrypoint (inside app/)
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
$env:FLASK_APP = "app.wsgi:app"
# Optional: $env:FLASK_DEBUG = "1"

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
export FLASK_APP=app.wsgi:app
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
```

## 🚢 Deploy (Render) — Step-by-Step
✅ This repo already includes render.yaml and app/wsgi.py auto-running migrations on startup, so you don’t need shell access on the free tier.

Option A — Blueprint (recommended, one click for Web + Postgres)
1. Push repo to GitHub (main branch).
2. In Render → Blueprints → New from Blueprint
   - Repo: `NoellaButi/code-banking-app`
   - Branch: `main`
   - Blueprint name: e.g., `noellabuti-code-banking-app-blueprint`
3. Review render.yaml and click Deploy Blueprint.
   Render will create:
   - banklite-db (Postgres, free)
   - banklite-web (Python web service, free)
4. Wait until banklite-web shows Live.
5. Health check → open:
```arduino
https://banklite-web.onrender.com/ping
```
(returns ok)
6. Open the app:
```arduino
https://banklite-web.onrender.com/
```

Blueprint config
- Build: `pip install --upgrade pip && pip install -r requirements.txt`
- Start: `gunicorn app.wsgi:app`
- Env vars:
  - `FLASK_APP=app.wsgi:app`
  - `SECRET_KEY (generated)`
  - `SQLALCHEMY_DATABASE_URI` (auto-wired to Postgres)
- Migrations: auto-run on startup via app/wsgi.py.

Option B — Manual Web Service + Database

1. Create a Web Service from repo.
   - Runtime: **Python**
   - Build: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start: `gunicorn app.wsgi:app`
   - Add env: `SECRET_KEY=some-random-string`
2. Create Postgres DB (free).
   - In service → **Environment** → set:
     ```ini
     SQLALCHEMY_DATABASE_URI=${DATABASE_URL}
     ```
     (from Render dropdown)
3. Deploy → check `/ping` → open `/.`

Option C — SQLite (demo only)

1. In service → Environment → set
   ```ini
   SQLALCHEMY_DATABASE_URI=sqlite:///banklite.db
   ```
2. Deploy → app will use SQLite.
3. Switch to Postgres later by removing override.

---

Shipping updates
- Code changes → push to main → auto-deploy.
- Schema changes → run locally:
  ```bash
  flask db migrate -m "add something"
  flask db upgrade
  git add migrations
  git commit -m "migrations: add something"
  git push origin main
  ```
  Render redeploys → app/wsgi.py auto-applies migrations.

Notes
- Free tier spins down after inactivity (~30–60s cold start).
- Region oregon.
- Starter plan ($7/mo) unlocks shell, persistent disks, zero downtime.

---

## 🔮 Roadmap
- JWT for API clients
- Pagination/filters on transactions
- CSV export of statements
- Admin role
- Docker Compose (app + Postgres)

📜 License
MIT (see [LICENSE](LICENSE))

---
