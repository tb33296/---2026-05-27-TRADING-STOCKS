from config.config import INSTRUMENT_MASTER_PATH
import json


def test_raw_reliance():

    with open(
        INSTRUMENT_MASTER_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    count = 0

    for row in data:

        symbol = str(
            row.get("symbol", "")
        ).upper()

        if "RELIANCE" in symbol:

            count += 1

            print(row)

            if count >= 10:
                break

    print(
        f"\nTotal Matches: {count}"
    )