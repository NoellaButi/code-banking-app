# test_api.py
from decimal import Decimal

from app.extensions import db
from app.models import User, Account, Transaction

def login(client, email, password):
    return client.post(
        "/auth/login",
        data = {"email": email, "password": password},
        follow_redirects = True,
    )

def api_create_account(client, name = "Checking", type_ = "Checking", opening = "0.00"):
    return client.post(
        "/api/accounts",
        json = {"name": name, "type": type_, "opening": opening},
    )

def test_api_list_accounts_empty(client, app):
    with app.app_context():
        u = User(email = "x@y.com")
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

    login(client, "x@y.com", "pw")
    resp = client.get("/api/accounts")
    assert resp.status_code == 200
    assert resp.json == []

def test_api_create_account_and_list(client, app):
    # Create user and login
    with app.app_context():
        u = User(email = "a@b.com")
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

    login(client, "a@b.com", "pw")

    # Create account via API
    r = api_create_account(client, name = "Main", type_ = "Checking", opening = "25.50")
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Main"
    assert data["type"] == "Checking"
    assert data["opening"] == "25.50"

    # List accounts
    r = client.get("/api/accounts")
    assert r.status_code == 200
    accs = r.get_json()
    assert len(accs) == 1
    assert accs[0]["name"] == "Main"

def test_api_deposit_withdraw(client, app):
    with app.app_context():
        u = User(email = "d@e.com")
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

    login(client, "d@e.com", "pw")

    # Create empty account
    r = api_create_account(client, name = "Wallet", type_ = "Checking", opening = "0.00")
    assert r.status_code == 201
    acc_id = r.get_json()["id"]

    # Deposit 50.00
    r = client.get("/api/transactions/deposit", json = {"account_id": acc_id, "amount": "50.00"})
    assert r.status_code == 201
    assert r.get_json()[kind] == "deposit"

    # Withdraw 20.00
    r = client.post("/api/transactions/withdraw", json = {"account_id": acc_id, "amount": "50.00"})
    assert r.status_code == 201
    assert r.get_json()[kind] == "withdraw"

    # Verify balance from DB
    with app.app_context():
        acc = db.session.get(Account, acc_id)
        assert acc.balance == Decimal("30.00")

        # And two transactions exist
        tx = Transaction.query.filter_by(account_id = acc_id).all()
        kinds = sorted(t.kind for t in tx)
        assert kinds == ["deposit", "withdraw"]

def test_api_transfer(client, app):
    with app.app_context():
        u = User(email = "t@t.com")
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

    login(client, "t@t.com", "pw")

    # src with 100, dst with 0
    r1 = api_create_account(client, name = "Src", type_ = "Checking", opening = "100.00")
    r2 = api_create_account(client, name = "Dst", type_ = "Savings", opening = "0.00")
    src_id = r1.get_json()["id"]
    dst_id = r2.get_json()["id"]

    # Transfer 25.00
    r = client.post("/api/transactions/transfer", json = {"src": src_id, "dst": dst_id, "amount": "25.00"})
    assert r.status_code == 201
    t = r.get_json()
    assert t["kind"] == "transfer"
    assert t["account_id"] == src_id
    assert t["related_account_id"] == dst_id

    # Verify balances
    with app.app_context():
        src = db.session.get(Account, src_id)
        dst = db.session.get(Account, dst_id)
        assert src.balance == Decimal("75.00")
        assert dst.balance == Decimal("25.00")

def test_api_forbid_cross_user_access(client, app):
    # user1 (owner)
    with app.app_context():
        u1 = User(email = "u1@ex.com"); u1.set_password("pw1")
        u2 = User(email = "u2@ex.com"); u2.set_password("pw2")
        db.session.add_all([u1, u2]); db.session.commit()

    # Create an account for user2 directly in DB
    a2 = Account(user_id = u2.id, name = "Other", type = "Checking")
    db.session.add(a2); db.session.commit()
    other_acc_id = a2.id

    # Login as user1
    login(client, "u1@ex.com", "pw1")

    # Try to deposit into user2's account -> forbidden
    r = client.post("/api/transactions/deposit", json = {"account_id": other_acc_id, "amount": "5.00"})
    assert r.status_code == 403