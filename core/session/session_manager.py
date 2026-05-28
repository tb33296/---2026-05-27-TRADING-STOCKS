# core/session/session_manager.py

from datetime import datetime, timedelta
from typing import Optional

from config.config import (
    SESSION_TIMEOUT_MINUTES,
    SESSION_REFRESH_BUFFER_MINUTES,
    MAX_SESSION_REFRESH_FAILURES
)

from core.auth.auth_manager import AuthManager
from core.logging_manager import LoggingManager


class SessionManager:
    """
    Handles authentication session lifecycle.
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.auth_manager = AuthManager()

        self.session_start_time: Optional[datetime] = None

        self.last_refresh_time: Optional[datetime] = None

        self.refresh_failure_count = 0

    def start_session(self) -> bool:
        """
        Start SmartAPI session.
        """

        try:

            self.logger.info(
                "Starting SmartAPI session"
            )

            success = self.auth_manager.login()

            if not success:

                self.logger.error(
                    "Failed to start session"
                )

                return False

            current_time = datetime.now()

            self.session_start_time = current_time

            self.last_refresh_time = current_time

            self.refresh_failure_count = 0

            self.logger.info(
                "Session started successfully"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Session start failed: {error}"
            )

            return False

    def refresh_session(self) -> bool:
        """
        Refresh SmartAPI session.
        """

        try:

            self.logger.info(
                "Refreshing session"
            )

            success = (
                self.auth_manager.refresh_session()
            )

            if not success:

                self.refresh_failure_count += 1

                self.logger.error(
                    f"Session refresh failed "
                    f"({self.refresh_failure_count})"
                )

                return False

            self.last_refresh_time = datetime.now()

            self.refresh_failure_count = 0

            self.logger.info(
                "Session refreshed successfully"
            )

            return True

        except Exception as error:

            self.refresh_failure_count += 1

            self.logger.error(
                f"Session refresh exception: {error}"
            )

            return False

    def is_session_alive(self) -> bool:
        """
        Validate session state.
        """

        try:

            if not self.auth_manager.is_session_valid():

                self.logger.warning(
                    "Auth manager reports invalid session"
                )

                return False

            if self.session_start_time is None:

                self.logger.warning(
                    "Session start time missing"
                )

                return False

            session_age = (
                datetime.now() - self.session_start_time
            )

            max_age = timedelta(
                minutes=SESSION_TIMEOUT_MINUTES
            )

            if session_age > max_age:

                self.logger.warning(
                    "Session expired by timeout"
                )

                return False

            if (
                self.refresh_failure_count >=
                MAX_SESSION_REFRESH_FAILURES
            ):

                self.logger.error(
                    "Maximum session refresh failures reached"
                )

                return False

            return True

        except Exception as error:

            self.logger.error(
                f"Session validation failed: {error}"
            )

            return False

    def should_refresh_session(self) -> bool:
        """
        Determine whether session refresh is required.
        """

        try:

            if self.last_refresh_time is None:
                return True

            refresh_age = (
                datetime.now() - self.last_refresh_time
            )

            refresh_threshold = timedelta(
                minutes=(
                    SESSION_TIMEOUT_MINUTES -
                    SESSION_REFRESH_BUFFER_MINUTES
                )
            )

            return refresh_age >= refresh_threshold

        except Exception as error:

            self.logger.error(
                f"Refresh threshold check failed: {error}"
            )

            return False

    def get_feed_token(self) -> Optional[str]:
        """
        Return current feed token.
        """

        return self.auth_manager.get_feed_token()

    def get_auth_manager(self) -> AuthManager:
        """
        Return auth manager instance.
        """

        return self.auth_manager

    def logout(self) -> None:
        """
        Logout active session.
        """

        try:

            self.auth_manager.logout()

            self.logger.info(
                "Session logout successful"
            )

        except Exception as error:

            self.logger.error(
                f"Session logout failed: {error}"
            )

    def get_session_age_minutes(self) -> float:
        """
        Return session age in minutes.
        """

        if self.session_start_time is None:
            return 0.0

        age = (
            datetime.now() -
            self.session_start_time
        )

        return round(
            age.total_seconds() / 60,
            2
        )

    def get_refresh_failure_count(self) -> int:
        """
        Return refresh failure count.
        """

        return self.refresh_failure_count
