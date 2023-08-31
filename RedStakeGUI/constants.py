import os
from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(ROOT, "data")

JSON_SETTINGS_PATH = os.path.join(DATA_DIRECTORY, "settings.json")
if not os.path.exists(JSON_SETTINGS_PATH):
    with open(JSON_SETTINGS_PATH, "w") as file:
        settings = {
            "sender_email_address": "",
            "sender_email_password": "",
            "receiever_email_address": "",
        }
        json.dump(settings, file)


# SERVER_DIRECTORY = "\\server"
# Off-site Test Directory
SERVER_DIRECTORY = os.path.join(ROOT, "TESTserver")
SERVER_ACCESS_DIRECTORY = os.path.join(SERVER_DIRECTORY, "access")
QUOTES_DIRECTORY = os.path.join(SERVER_ACCESS_DIRECTORY, "quotes")


if not os.path.exists(QUOTES_DIRECTORY):
    os.makedirs(QUOTES_DIRECTORY)


INTAKE_LABELS = os.path.join(DATA_DIRECTORY, "intake_labels.txt")
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())
