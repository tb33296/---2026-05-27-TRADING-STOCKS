
# core/auth/auth_manager.py

from datetime import datetime
from typing import Any, Optional

import pyotp
import time

from SmartApi import SmartConnect

from config.config import (
    LOGIN_RETRY_LIMIT,
    LOGIN_RETRY_DELAY
)

from core.logging_manager import LoggingManager

from loginInfo import (
    API_KEY,
    CLIENT_ID,
    PIN,
    TOTP_SECRET
)


class AuthManager:
    """
    SmartAPI authentication manager.
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.smart_api: Optional[SmartConnect] = None

        self.jwt_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.feed_token: Optional[str] = None

        self.user_profile: Optional[dict[str, Any]] = None

        self.login_time: Optional[datetime] = None

    def generate_totp(self) -> str:
        """
        Generate TOTP code.
        """

        if TOTP_SECRET is None:
            raise RuntimeError(
                "TOTP_SECRET missing in .env"
            )

        try:

            totp = pyotp.TOTP(TOTP_SECRET)

            return str(totp.now())

        except Exception as error:

            self.logger.error(
                f"TOTP generation failed: {error}"
            )

            raise

    def login(self) -> bool:
        """
        Login to SmartAPI.
        """

        retry_count = 0

        while retry_count < LOGIN_RETRY_LIMIT:

            try:

                self.logger.info(
                    "Attempting SmartAPI login"
                )

                if API_KEY is None:
                    raise RuntimeError(
                        "API_KEY missing in .env"
                    )

                if CLIENT_ID is None:
                    raise RuntimeError(
                        "CLIENT_ID missing in .env"
                    )

                if PIN is None:
                    raise RuntimeError(
                        "PIN missing in .env"
                    )

                self.smart_api = SmartConnect(
                    api_key=API_KEY
                )

                totp = self.generate_totp()

                response: Any = self.smart_api.generateSession(
                    CLIENT_ID,
                    PIN,
                    totp
                )

                if not isinstance(response, dict):
                    raise RuntimeError(
                        f"Invalid login response type: {type(response)}"
                    )

                if not response.get("status"):
                    raise RuntimeError(
                        f"Login failed: {response}"
                    )

                data = response.get("data", {})

                if not isinstance(data, dict):
                    raise RuntimeError(
                        "Invalid response data"
                    )

                self.jwt_token = data.get("jwtToken")
                self.refresh_token = data.get("refreshToken")

                if not self.jwt_token:
                    raise RuntimeError(
                        "JWT token missing"
                    )

                if self.smart_api is None:
                    raise RuntimeError(
                        "SmartAPI instance missing"
                    )

                self.feed_token = str(
                    self.smart_api.getfeedToken()
                )

                profile_response: Any = (
                    self.smart_api.getProfile(
                        self.refresh_token
                    )
                )

                if isinstance(profile_response, dict):
                    self.user_profile = profile_response
                else:
                    self.user_profile = {}

                self.login_time = datetime.now()

                self.logger.info(
                    "SmartAPI login successful"
                )

                return True

            except Exception as error:

                retry_count += 1

                self.logger.error(
                    f"Login attempt {retry_count} failed: {error}"
                )

                time.sleep(LOGIN_RETRY_DELAY)

        self.logger.error(
            "SmartAPI login failed after retries"
        )

        return False

    def refresh_session(self) -> bool:
        """
        Refresh SmartAPI session.
        """

        try:

            if self.smart_api is None:
                raise RuntimeError(
                    "SmartAPI not initialized"
                )

            if self.refresh_token is None:
                raise RuntimeError(
                    "Refresh token missing"
                )

            response: Any = self.smart_api.generateToken(
                self.refresh_token
            )

            if not isinstance(response, dict):
                raise RuntimeError(
                    "Invalid refresh response"
                )

            if not response.get("status"):
                raise RuntimeError(
                    f"Session refresh failed: {response}"
                )

            data = response.get("data", {})

            if not isinstance(data, dict):
                raise RuntimeError(
                    "Invalid refresh data"
                )

            self.jwt_token = data.get("jwtToken")

            self.feed_token = str(
                self.smart_api.getfeedToken()
            )

            self.logger.info(
                "Session refreshed successfully"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Session refresh failed: {error}"
            )

            return False

    def logout(self) -> None:
        """
        Logout from SmartAPI.
        """

        try:

            if (
                self.smart_api is not None
                and CLIENT_ID is not None
            ):

                self.smart_api.terminateSession(
                    CLIENT_ID
                )

                self.logger.info(
                    "SmartAPI logout successful"
                )

        except Exception as error:

            self.logger.error(
                f"Logout failed: {error}"
            )

    def get_feed_token(self) -> Optional[str]:
        """
        Return feed token.
        """

        return self.feed_token

    def is_session_valid(self) -> bool:
        """
        Validate current session.
        """

        return (
            self.smart_api is not None
            and self.jwt_token is not None
            and self.feed_token is not None
        )

    def get_user_profile(
        self
    ) -> Optional[dict[str, Any]]:
        """
        Return user profile.
        """

        return self.user_profile
