# test_auth.py

from core.logging_manager import LoggingManager
from core.auth.auth_manager import AuthManager


LoggingManager.initialize()

auth = AuthManager()

success = auth.login()

print(f"Login Success: {success}")

if success:

    print("Session Valid:", auth.is_session_valid())

    print("Feed Token:", auth.get_feed_token() is not None)

    print("User Profile:")
    print(auth.get_user_profile())

    auth.logout()