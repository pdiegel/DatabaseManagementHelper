import json
import os
from typing import Tuple

from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(ROOT, "data")

JSON_SETTINGS_PATH = os.path.join(DATA_DIRECTORY, "settings.json")


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
    with open(JSON_SETTINGS_PATH, "r") as file:
        settings = json.load(file)

    sender = settings.get("sender_email_address", "")
    receiver = settings.get("receiever_email_address", "")
    password = settings.get("sender_email_password", "")
    return sender, receiver, password


if not os.path.exists(JSON_SETTINGS_PATH):
    save_email_settings()

SERVER_DIRECTORY = "\\server"
# Off-site Test Directory
# SERVER_DIRECTORY = os.path.join(ROOT, "TESTserver")
SERVER_ACCESS_DIRECTORY = os.path.join(SERVER_DIRECTORY, "access")
QUOTES_DIRECTORY = os.path.join(SERVER_ACCESS_DIRECTORY, "quotes")


if not os.path.exists(QUOTES_DIRECTORY):
    os.makedirs(QUOTES_DIRECTORY)


INTAKE_LABELS = os.path.join(DATA_DIRECTORY, "intake_labels.txt")
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())
