import pytest
import os
from database import get_db_connection, init_db
from constants import AccountType
from app.repositories import customer_repo, account_repo

TEST_DB_PATH = "data/test_db.db"

@pytest.fixture
def db():
    old_db = os.environ.get("DB_PATH")
    os.environ["DB_PATH"] = TEST_DB_PATH

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    init_db()

    conn = get_db_connection()

    yield conn

    conn.close()

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    if old_db is None:
        os.environ.pop("DB_PATH", None)
    else:
        os.environ["DB_PATH"] = old_db

@pytest.fixture
def customer(db):

    customer = customer_repo.create_customer(
        db,
        "Test",
        "User1",
        "TestUser1@gmail.com",
        "testuser1321",
        "+921234567890"
    )

    db.commit()

    return customer

@pytest.fixture
def second_customer(db):

    customer = customer_repo.create_customer(
        db,
        "Test",
        "User2",
        "TestUser2@gmail.com",
        "testuser2321",
        "+920987654321"
    )

    db.commit()

    return customer

@pytest.fixture
def account(db, customer):

    account = account_repo.create_account(
        db,
        customer.customer_id,
        AccountType.SAVINGS.value
    )

    db.commit()

    return account

@pytest.fixture
def second_account(db, customer):

    second_account = account_repo.create_account(
        db,
        customer.customer_id,
        AccountType.CHECKING.value
    )

    db.commit()

    return second_account