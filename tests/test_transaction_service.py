import pytest
from app.services import transaction_service
from app.repositories import account_repo, transaction_repo
from constants import Status, TransactionType

class TestDeposit:

    @pytest.mark.parametrize("amount", [1, 10, 100, 1000])
    def test_deposit_success(self, db, account, amount):
        old_balance = account.balance
        
        result = transaction_service.deposit(account.account_id, amount)

        transactions = transaction_repo.get_transaction_history(db, account.account_id)

        updated_account = account_repo.get_account_by_account_id(db, account.account_id)

        db.commit()

        assert result["success"] is True
        assert "new_balance" in result["data"]
        assert "msg" in result["data"]
        assert updated_account.balance == old_balance + amount
        assert result["data"]["new_balance"] == old_balance + amount
        assert len(transactions) == 1
        assert transactions[0].amount == amount
        assert transactions[0].transaction_type == TransactionType.CREDIT.value
    
    @pytest.mark.parametrize("amount, account_id", [(10, 99), (100, "999"), (1000, -10)])
    def test_deposit_no_account(self, db, amount, account_id):
        result = transaction_service.deposit(account_id, amount)

        assert result["success"] is False
        assert "source_account" in result["data"]
        assert "Account not found" in result["data"]["source_account"]
    
    @pytest.mark.parametrize("amount", [-1, -100, 0, -100000, 0.0005, -0.0003])
    def test_deposit_negative_amount(self, amount, account):
        result = transaction_service.deposit(account.account_id, amount)

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "more than 0.01" in result["data"]["amount"]
    
    @pytest.mark.parametrize("amount", [100001, 100000.01, 999999, 100000000000, 897192739138126])
    def test_deposit_greater_amount(self, amount, account):
        result = transaction_service.deposit(account.account_id, amount)

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "cannot deposit more than 100 thousand" in result["data"]["amount"]
    
    def test_deposit_closed_account(self, db, account):
        account_repo.change_account_status(
            db,
            account.account_id,
            Status.CLOSED.value
        )

        db.commit()

        result = transaction_service.deposit(account.account_id, 1000)

        assert result["success"] is False
        assert "source_account_status" in result["data"]
        assert "account was closed" in result["data"]["source_account_status"]



class TestWithdraw:

    @pytest.mark.parametrize("amount", [1, 10, 100, 1000])
    def test_withdraw_success(self, db, amount, account):
        old_balance = 10000
        
        cursor = db.cursor()
        
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_id = ?",
            (old_balance, account.account_id)
        )
        
        db.commit()

        result = transaction_service.withdraw(account.account_id, amount)

        transactions = transaction_repo.get_transaction_history(db, account.account_id)

        updated_account = account_repo.get_account_by_account_id(db, account.account_id)

        db.commit()

        assert result["success"] is True
        assert "new_balance" in result["data"]
        assert "msg" in result["data"]
        assert updated_account.balance == old_balance - amount
        assert result["data"]["new_balance"] == old_balance - amount
        assert len(transactions) == 1
        assert transactions[0].amount == amount
        assert transactions[0].transaction_type == TransactionType.DEBIT.value
    
    def test_withdraw_wrong_account_id(self, db):
        result = transaction_service.withdraw(999, 1000)

        assert result["success"] is False
        assert "source_account" in result["data"]
        assert "Account not found" in result["data"]["source_account"]
    
    def test_withdraw_blocked_account(self, db, account):
        account_repo.change_account_status(
            db,
            account.account_id,
            Status.BLOCKED.value
        )

        db.commit()
        
        result = transaction_service.withdraw(account.account_id, 1000)

        assert result["success"] is False
        assert "source_account_status" in result["data"]
        assert "account is not active" in result["data"]["source_account_status"]
    
    @pytest.mark.parametrize("amount", [-1, -100, 0, -100000, 0.0005, -0.0003])
    def test_withdraw_negative_amount(self, amount, account):
        result = transaction_service.withdraw(account.account_id, amount)

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "more than 0.01" in result["data"]["amount"]
    
    @pytest.mark.parametrize("amount", [100001, 100000.01, 999999, 100000000000, 897192739138126])
    def test_withdraw_greater_amount(self, amount, account):
        result = transaction_service.withdraw(account.account_id, amount)

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "Insufficient funds" in result["data"]["amount"]



class TestTransfer:

    @pytest.mark.parametrize("amount", [1, 10, 100, 1000])
    def test_transfer_success(self, db, account, second_account, amount):
        old_account_balance = 1000
        old_second_account_balance = 0
        cursor = db.cursor()
        
        cursor.executemany(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            [
                (1000, account.account_id),
                (0, second_account.account_id)
            ]
        )
        
        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            second_account.account_id,
            amount
        )

        transactions1 = transaction_repo.get_transaction_history(db, account.account_id)
        transactions2 = transaction_repo.get_transaction_history(db, second_account.account_id)

        updated_account1 = account_repo.get_account_by_account_id(db, account.account_id)
        updated_account2 = account_repo.get_account_by_account_id(db, second_account.account_id)

        db.commit()

        assert result["success"] is True
        assert "new_balance" in result["data"]
        assert "msg" in result["data"]
        assert result["data"]["new_balance"] == old_account_balance - amount
        assert updated_account1.balance == old_account_balance - amount
        assert updated_account2.balance == old_second_account_balance + amount
        assert len(transactions1) == 1
        assert len(transactions2) == 1
        assert transactions1[0].amount == amount
        assert transactions2[0].amount == amount
        assert transactions1[0].transaction_type == TransactionType.DEBIT.value
        assert transactions2[0].transaction_type == TransactionType.CREDIT.value
    
    def test_transfer_source_account_not_found(self, db, second_account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, second_account.account_id)        
        )

        db.commit()

        result = transaction_service.transfer(
            999,
            second_account.account_id,
            100
        )

        assert result["success"] is False
        assert "source_account" in result["data"]
        assert "not found" in result["data"]["source_account"]
    
    def test_transfer_target_account_not_found(self, db, account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)        
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            999,
            100
        )

        assert result["success"] is False
        assert "target_account" in result["data"]
        assert "not found" in result["data"]["target_account"]
    
    def test_transfer_account_mismatch(self, db, account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)        
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            account.account_id,
            100
        )

        assert result["success"] is False
        assert "account_mismatch" in result["data"]
    
    def test_transfer_blocked_source_account(self, db, account, second_account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)
        )

        account_repo.change_account_status(
            db,
            account.account_id,
            Status.BLOCKED.value
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            second_account.account_id,
            100
        )

        assert result["success"] is False
        assert "source_account_status" in result["data"]
        assert "not active" in result["data"]["source_account_status"]
    
    def test_transfer_blocked_target_account(self, db, account, second_account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)
        )

        account_repo.change_account_status(
            db,
            second_account.account_id,
            Status.BLOCKED.value
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            second_account.account_id,
            100
        )

        assert result["success"] is False
        assert "target_account_status" in result["data"]
        assert "not active" in result["data"]["target_account_status"]
    
    @pytest.mark.parametrize("amount", [-1, -100, 0, -100000, 0.0005, -0.0003])
    def test_transfer_negative_amount(self, amount, db, account, second_account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            second_account.account_id,
            amount
        )

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "more than 0.01" in result["data"]["amount"]
    
    @pytest.mark.parametrize("amount", [100001, 100000.01, 999999, 100000000000, 897192739138126])
    def test_transfer_greater_amount(slef, amount, db, account, second_account):

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,(1000, account.account_id)
        )

        db.commit()

        result = transaction_service.transfer(
            account.account_id,
            second_account.account_id,
            amount
        )

        assert result["success"] is False
        assert "amount" in result["data"]
        assert "Insufficient funds" in result["data"]["amount"]