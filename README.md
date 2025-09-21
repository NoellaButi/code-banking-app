# BankLite — Flask Banking App 🏦🌙💖  
Minimal banking demo with **Flask + SQLAlchemy**, authentication, HTML views, and a JSON API.

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)
![DB](https://img.shields.io/badge/database-Postgres-7957D5.svg)
![Tests](https://img.shields.io/badge/tests-pytest-6aa84f.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![CI](https://github.com/NoellaButi/code-banking-app/actions/workflows/ci.yml/badge.svg)

👉 [**Live Demo (Render)**](https://banklite-web.onrender.com/auth/login?next=%2F) 

![BankLite Login Page](docs/banklite_app_demo.png)

---

## ✨ Overview
BankLite is a teaching/demo banking backend.  
Users can sign up, create **Checking/Savings accounts**, and perform **deposits, withdrawals, and transfers**.  

It demonstrates:
- Flask app factory + blueprints  
- SQLAlchemy models & migrations  
- Flask-Login auth, CSRF protection  
- Business logic with **atomic transfers**  
- JSON serialization with Marshmallow  
- Tests with **pytest**

---

## 🔍 Features
- **Accounts**: Checking/Savings with opening balances  
- **Transactions**: Deposit, withdraw, transfer (atomic, double entry)  
- **Security**: Password hashing, CSRF-protected forms, session cookies  
- **JSON API**: List/create accounts, make transactions  
- **Frontend**: Dark + pink themed HTML templates  
- **Tests**: pytest unit tests and coverage  

---

## 🚦 Quickstart

### Local Setup
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
flask run
# http://127.0.0.1:5000
```
Run Tests
```bash
pytest -q
```

## 📁 Repository Layout
```bash
code-banking-app/
├─ app/                # main Flask app
│  ├─ models.py        # User, Account, Transaction
│  ├─ services.py      # deposit/withdraw/transfer logic
│  ├─ api.py           # JSON API endpoints
│  ├─ routes.py        # HTML routes
│  └─ templates/       # Jinja2 templates
├─ migrations/         # Alembic migrations
├─ tests/              # pytest tests
├─ .env.example        # sample config
├─ requirements.txt
└─ README.md
```

## 📊 Results
- Deployed on Render (Postgres + Gunicorn)
- Verified migrations auto-run on startup

## 🔮 Roadmap
- JWT support for API clients
- CSV export of transactions
- Admin dashboard
- Docker Compose setup

## 📜 License
MIT (see LICENSE)

---
