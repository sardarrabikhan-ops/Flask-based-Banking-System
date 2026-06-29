import pytest
from app.services import account_service
from app.repositories import account_repo, customer_repo
from constants import Status

class TestCloseAccount:

    def test_close_account_success(self, db, account):
        result = account_service.close_account(account.account_id)

        assert result["success"] is True

        close_account = result["data"]["account"]

        assert close_account.status == Status.CLOSED.value

        db_account = account_repo.get_account_by_account_id(db, close_account.account_id)

        db.commit()

        assert db_account.status == Status.CLOSED.value
    
    @pytest.mark.parametrize("account_id", [99, 999, 9999])
    def test_close_account_wrong_account_id(self, db, account_id):
        result = account_service.close_account(account_id)

        assert result["success"] is False
        assert "account_existence" in result["data"]
        assert "Account Not found." == result["data"]["account_existence"]
    
    def test_close_account_with_balance(self, db, account):
        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (1000, account.account_id)
        )

        db.commit()

        result = account_service.close_account(account.account_id)

        assert result["success"] is False
        assert "balance_existence" in result["data"]

        db_account = account_repo.get_account_by_account_id(db, account.account_id)

        db.commit()

        assert db_account.status == Status.ACTIVE.value



class TestGetAccountsForCustomer:

    def test_get_accounts_for_customer_success(self, customer, account, second_account):
        result = account_service.get_accounts_for_customer(customer.customer_id)

        assert result["success"] is True
        
        accounts = result["data"]["accounts"]

        assert len(accounts) == 2

        returned_acc_ids = {a.account_id for a in accounts}
        expected_acc_ids = {account.account_id, second_account.account_id}

        returned_cust_ids = {a.customer_id for a in accounts}
        expected_cust_ids = {account.customer_id, second_account.customer_id}

        assert returned_acc_ids == expected_acc_ids
        assert returned_cust_ids == expected_cust_ids
    
    @pytest.mark.parametrize("customer_id", [99, 999, 9999])
    def test_get_accounts_for_customer_wrong_customer_id(self, db, customer_id):
        result = account_service.get_accounts_for_customer(customer_id)

        assert result["success"] is False
        assert "customer" in result["data"]
        assert "Customer not found." == result["data"]["customer"]
    
    def test_get_accounts_for_customer_no_account(self, second_customer):
        result = account_service.get_accounts_for_customer(second_customer.customer_id)

        assert result["success"] is False
        assert "accounts" in result["data"]
    
    def test_get_accounts_for_customer_blocked_customer(self, db, customer, account):
        customer_repo.change_customer_status(
            db,
            customer.customer_id,
            Status.BLOCKED.value
            )
        
        db.commit()

        result = account_service.get_accounts_for_customer(customer.customer_id)

        assert result["success"] is False
        assert "customer" in result["data"]



class TestGetAccountById:

    def test_get_account_by_id_success(self, account):
        result = account_service.get_account_by_id(account.account_id)

        assert result["success"] is True
        assert result["data"]["account"].account_id == account.account_id
    
    @pytest.mark.parametrize("account_id", [99, 999, 9999])
    def test_get_account_by_id_wrong_account_id(self, db, account_id):
        result = account_service.get_account_by_id(account_id)

        assert result["success"] is False
        assert "account" in result["data"]
        assert "Account not found." == result["data"]["account"]
    
    def test_get_account_by_id_blocked_account(self, db, account):
        account_repo.change_account_status(
            db,
            account.account_id,
            Status.BLOCKED.value
        )

        db.commit()

        result = account_service.get_account_by_id(account.account_id)

        assert result["success"] is False
        assert "account" in result["data"]
        assert "not active" in result["data"]["account"]