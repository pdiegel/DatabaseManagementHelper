import json
from pathlib import Path
from typing import Tuple

from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP

MAIN_TITLE = "Red Stake Surveyors, Inc."
ROOT = Path(__file__).parent
DATA_DIRECTORY = ROOT / "data"
JSON_SETTINGS_PATH = DATA_DIRECTORY / "settings.json"


def save_email_settings(
    sender: str = "", password: str = "", receiver: str = ""
) -> None:
    with open(JSON_SETTINGS_PATH, "w") as file:
        settings = {
            "sender_email_address": sender,
            "sender_email_password": password,
            "receiever_email_address": receiver,
        }
        json.dump(settings, file)


def get_email_settings() -> Tuple[str, str, str]:
    """This method will return the email settings from the
    settings.json file.

    Returns:
        Tuple[str, str, str]: The sender email address, receiver
            email address, and sender email password.
    """
    # Error handling for corrupted settings file
    try:
        with open(JSON_SETTINGS_PATH, "r") as file:
            settings = json.load(file)
    except json.decoder.JSONDecodeError:
        save_email_settings()
        with open(JSON_SETTINGS_PATH, "r") as file:
            settings = json.load(file)

    sender = settings.get("sender_email_address", "")
    receiver = settings.get("receiever_email_address", "")
    password = settings.get("sender_email_password", "")
    return sender, receiver, password


if not JSON_SETTINGS_PATH.exists():
    save_email_settings()

SERVER_DIRECTORY = Path("//server")
# Off-site Test Directory
# SERVER_DIRECTORY = os.path.join(ROOT, "TESTserver")
SERVER_ACCESS_DIRECTORY = SERVER_DIRECTORY / "access"
QUOTES_DIRECTORY = SERVER_ACCESS_DIRECTORY / "quotes"
QUOTES_DIRECTORY = Path(str(QUOTES_DIRECTORY).replace("\\", "\\\\", 1))
print(QUOTES_DIRECTORY)

if not QUOTES_DIRECTORY.exists():
    QUOTES_DIRECTORY.mkdir(parents=True)


INTAKE_LABELS = DATA_DIRECTORY / "intake_labels.txt"
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())
