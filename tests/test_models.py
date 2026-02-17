from models import User

def test_user_password_hashing_behaves_correctly():
    """Test that set_passowrd hashes the password and check_password verifies it."""
    user = User(username="testuser")
    user.set_password("testpassword")

    # Password hash should be set and not be the plain password
    assert user.password_hash is not None
    assert user.password_hash !="testpassword"

    # Correct password should return True
    assert user.check_password("testpassword") is True

    # Incorrect passowrd should return False
    assert user.check_password("wrongpassword") is False