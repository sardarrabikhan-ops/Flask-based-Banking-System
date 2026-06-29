import pytest
from app.services import auth_service
from app.repositories import customer_repo
from constants import Status, AccountType

TEST_PASSWORD1 = "testuser1321"
TEST_EMAIL1 = "TestUser1@gmail.com"
TEST_PASSWORD2 = "testuser2321"
TEST_EMAIL2 = "TestUser2@gmail.com"

class TestRegister:

    def test_register_success(self, db):
        result = auth_service.register(
            "John",
            "Doe",
            "John@Example.com",
            "+921111111111",
            "Password123!",
            "Password123!"
        )

        assert result["success"] is True

        customer = result["data"]["customer"]
        account = result["data"]["account"]

        assert customer.email == "john@example.com"
        assert customer.customer_id == account.customer_id
        assert account.balance == 0
        assert account.status == Status.ACTIVE.value
        assert account.account_type == AccountType.SAVINGS.value
    
    def test_register_duplicate_email(self, db, customer):
        result = auth_service.register(
            "John",
            "Doe",
            customer.email,
            "+921111111111",
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "email" in result["data"]
    
    def test_register_duplicate_phone(self, db, customer):
        result = auth_service.register(
            "John",
            "Doe",
            "John@Example.com",
            customer.phone,
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "phone" in result["data"]
    
    @pytest.mark.parametrize("email", [("abcd"), ("invalid-email"), ("example.example")])
    def test_register_invalid_email(self, db, email):
        result = auth_service.register(
            "John",
            "Doe",
            email,
            "+921111111111",
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "email" in result["data"]
    
    @pytest.mark.parametrize("phone", [("1234567890"), ("abcdefghijl"), ("abc1234567890"), ("03331238764")])
    def test_register_invalid_phone(self, db, phone):
        result = auth_service.register(
            "John",
            "Doe",
            "John@Example.com",
            phone,
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "phone" in result["data"]
    
    def test_register_password_mismatch(self, db):
        result = auth_service.register(
            "John",
            "Doe",
            "John@Example.com",
            "+921111111111",
            "Password123!",
            "Password321!"
        )

        assert result["success"] is False
        assert "confirm_password" in result["data"]
    
    @pytest.mark.parametrize("password", [("abcde"), ("abc123"), ("password"), ("qwerty123")])
    def test_register_invalid_password(self, db, password):
        result = auth_service.register(
            "John",
            "Doe",
            "John@Example.com",
            "+921111111111",
            password,
            password
        )

        assert result["success"] is False
        assert "password" in result["data"]
    
    @pytest.mark.parametrize("firstname", ["first-name", "ab", "invalid-firstname"])
    def test_register_invalid_firstname(self, db, firstname):
        result = auth_service.register(
            firstname,
            "Doe",
            "John@Example.com",
            "+921111111111",
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "firstname" in result["data"]
    
    @pytest.mark.parametrize("lastname", ["last-name", "cd", "invalid-lastname"])
    def test_register_invalid_lastname(self, db, lastname):
        result = auth_service.register(
            "Jhon",
            lastname,
            "John@Example.com",
            "+921111111111",
            "Password123!",
            "Password123!"
        )

        assert result["success"] is False
        assert "lastname" in result["data"]




class TestLogin:

    def test_login_success(self, db, customer):
        result = auth_service.login(
            TEST_EMAIL1,
            TEST_PASSWORD1
        )

        assert result["success"] is True
        
        user = result["data"]["user"]

        assert user.customer_id == customer.customer_id
        assert user.email == customer.email
    
    def test_login_unknown_user(self, db):
        result = auth_service.login(
            "example@example.com",
            TEST_PASSWORD1
        )

        assert result["success"] is False
        assert "user_existence" in result["data"]
    
    def test_login_blocked_user(self, db, second_customer):
        customer_repo.change_customer_status(
            db,
            second_customer.customer_id,
            Status.BLOCKED.value
        )
        
        db.commit()

        result = auth_service.login(
            TEST_EMAIL2,
            TEST_PASSWORD2
        )

        assert result["success"] is False
        assert "account_locked" in result["data"]
    
    def test_login_wrong_password(self, db, customer):
        result = auth_service.login(
            TEST_EMAIL1, 
            "wrongpassword"
            )

        assert result["success"] is False
        assert "password" in result["data"]
        assert result["data"]["password"] == "Incorrect password!"
    
    def test_login_3failed_attempts(self, db, customer):
        auth_service.login(TEST_EMAIL1, "wrong")
        auth_service.login(TEST_EMAIL1, "wrong")
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "account_locked" in result["data"]
        assert "Account is locked for 30 seconds!" == result["data"]["account_locked"]
    
    def test_login_temporarily_locked_user(self, db, customer):
        for _ in range(3):
            auth_service.login(TEST_EMAIL1, "wrong")
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "account_locked" in result["data"]
        assert "User is locked temporarily! Try again after" in result["data"]["account_locked"]
    
    def test_login_5failed_attempts(self, db, customer):
        customer_repo.update_failed_attempts(db, customer.customer_id, 4)
        customer_repo.update_lock_until(db, customer.customer_id, None)

        db.commit()
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "Account is locked for 5 minutes!" == result["data"]["account_locked"]
    
    def test_login_7failed_attempts(self, db, customer):
        customer_repo.update_failed_attempts(db, customer.customer_id, 6)
        customer_repo.update_lock_until(db, customer.customer_id, None)

        db.commit()
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "Account is locked for 30 minutes!" == result["data"]["account_locked"]
    
    def test_login_10failed_attempts(self, db, customer):
        customer_repo.update_failed_attempts(db, customer.customer_id, 9)
        customer_repo.update_lock_until(db, customer.customer_id, None)

        db.commit()
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "Account is locked for 1 hours!" == result["data"]["account_locked"]
    
    def test_login_warning(self, db, customer):
        customer_repo.update_failed_attempts(db, customer.customer_id, 7)
        customer_repo.update_lock_until(db, customer.customer_id, None)

        db.commit()
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "Warning!" in result["data"]["account_locked"]
    

    
    def test_login_15failed_attempts(self, db, customer):
        customer_repo.update_failed_attempts(db, customer.customer_id, 14)
        customer_repo.update_lock_until(db, customer.customer_id, None)

        db.commit()
        
        result = auth_service.login(TEST_EMAIL1, "wrong")

        assert result["success"] is False
        assert "account_locked" in result["data"]
        assert "User is blocked!" in result["data"]["account_locked"]
    
    # def test_login_temporarily_locked_user(self, db, customer):
    #     lock_until = (datetime.now() + timedelta(hours=1)).timestamp()

    #     customer_repo.update_lock_until(
    #         db,
    #         customer.customer_id,
    #         lock_until
    #     )

    #     db.commit()

    #     result = auth_service.login(
    #         TEST_EMAIL1, 
    #         TEST_PASSWORD1
    #         )

    #     assert result["success"] is False
    #     assert "account_locked" in result["data"]
    #     assert "User is locked temporarily!" in result["data"]["account_locked"]