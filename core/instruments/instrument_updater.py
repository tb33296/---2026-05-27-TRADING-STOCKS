# core/instruments/instrument_updater.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

from config.config import (
    INSTRUMENT_MASTER_PATH
)

from core.logging_manager import (
    LoggingManager
)


class InstrumentUpdater:
    """
    Downloads and validates
    Angel One instrument master.

    Responsibilities:
    - download latest instrument file
    - validate JSON
    - save locally
    """

    INSTRUMENT_URL = (
        "https://margincalculator.angelbroking.com/"
        "OpenAPI_File/files/OpenAPIScripMaster.json"
    )

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.output_file = Path(
            INSTRUMENT_MASTER_PATH
        )

    def download(self) -> bool:
        """
        Download latest instrument master.
        """

        try:

            self.logger.info(
                "Downloading instrument master"
            )

            response = requests.get(
                self.INSTRUMENT_URL,
                timeout=120
            )

            response.raise_for_status()

            data: Any = response.json()

            if not isinstance(data, list):

                self.logger.error(
                    "Invalid instrument master format"
                )

                return False

            if len(data) == 0:

                self.logger.error(
                    "Instrument master is empty"
                )

                return False

            self.output_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                self.output_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    separators=(",", ":")
                )

            self.logger.info(
                f"Downloaded "
                f"{len(data)} instruments"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Instrument download failed: "
                f"{error}"
            )

            return False

    def validate(self) -> bool:
        """
        Validate local instrument file.
        """

        try:

            if not self.output_file.exists():

                self.logger.error(
                    "Instrument file missing"
                )

                return False

            if self.output_file.stat().st_size == 0:

                self.logger.error(
                    "Instrument file empty"
                )

                return False

            with open(
                self.output_file,
                "r",
                encoding="utf-8"
            ) as file:

                data: Any = json.load(file)

            if not isinstance(data, list):

                self.logger.error(
                    "Invalid instrument file"
                )

                return False

            if len(data) == 0:

                self.logger.error(
                    "Instrument list empty"
                )

                return False

            return True

        except Exception as error:

            self.logger.error(
                f"Instrument validation failed: "
                f"{error}"
            )

            return False

    def update(self) -> bool:
        """
        Download and validate.
        """

        if not self.download():

            return False

        return self.validate()