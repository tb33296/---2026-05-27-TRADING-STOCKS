
# tests/test_auth_runtime.py

from core.auth.auth_manager import AuthManager
from core.logging_manager import LoggingManager


def test_auth_runtime() -> None:

    LoggingManager.initialize()

    auth = AuthManager()

    success = auth.login()

    assert success is True

    assert auth.is_session_valid() is True

    assert auth.get_feed_token() is not None

    profile = auth.get_user_profile()

    assert profile is not None

    auth.logout()

