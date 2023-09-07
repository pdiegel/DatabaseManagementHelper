import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP

from RedStakeGUI.models.access_database import AccessDB
from RedStakeGUI.models.encryption_manager import EncryptionManager
from RedStakeGUI.models.settings_manager import SettingsManager
import base64

MAIN_TITLE = "Red Stake Surveyors, Inc."

ROOT = Path(__file__).parent
DATA_DIRECTORY = ROOT / "data"
ENV_PATH = DATA_DIRECTORY / ".env"
ENV_VARIABLES = (
    "SENDER_EMAIL_ADDRESS",
    "SENDER_EMAIL_PASSWORD",
    "RECIPIENT_EMAIL_ADDRESS",
    "ENCRYPTION_KEY",
)

if not ENV_PATH.exists():
    with open(ENV_PATH, "w") as file:
        for variable in ENV_VARIABLES:
            file.write(f"{variable}=\n")
        logging.info("Created .env file with empty variables.")


load_dotenv(ENV_PATH)


encryption_key_string = os.getenv("ENCRYPTION_KEY")
print(f"Type of key: {type(encryption_key_string)}")
print(f"Key being used: {encryption_key_string}")
ENCRYPTION_MANAGER = EncryptionManager(encryption_key_string)


print(f"Type of key2: {type(ENCRYPTION_MANAGER.key)}")
print(f"Key being used2: {ENCRYPTION_MANAGER.key}")
ENCRYPTION_KEY = base64.urlsafe_b64decode(ENCRYPTION_MANAGER.key).decode()

SETTINGS_MANAGER = SettingsManager(ENV_PATH, ENCRYPTION_MANAGER)
SETTINGS_MANAGER.update_env_file("ENCRYPTION_KEY", ENCRYPTION_KEY)


def fix_server_directory_path(path: Path) -> str:
    """This method will fix the path to the server directory.
    The server directory path is used to open the quotes on the server.

    By default, the Path object is replacing the network double slash
    with a single slash. This method will replace the single slash
    with a double slash.

    Args:
        path (Path): The path to the quote on the server.

    Returns:
        Path: The fixed path to the quote on the server.
    """
    path = Path(str(path).replace("\\", "\\\\", 1))
    return path


# Off-site Test Directory
# SERVER_DIRECTORY = os.path.join(ROOT, "TESTserver")
SERVER_DIRECTORY = Path("//server")

SERVER_ACCESS_DIRECTORY = SERVER_DIRECTORY / "access"
QUOTES_DIRECTORY = SERVER_ACCESS_DIRECTORY / "quotes"
QUOTES_DIRECTORY = fix_server_directory_path(QUOTES_DIRECTORY)

if not QUOTES_DIRECTORY.exists():
    QUOTES_DIRECTORY.mkdir(parents=True)


INTAKE_LABELS = DATA_DIRECTORY / "intake_labels.txt"
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())

ACCESS_DATABASE_PATH = (
    SERVER_ACCESS_DIRECTORY / "Database Backup" / "MainDB_be.accdb"
)
ACCESS_DATABASE_PATH = fix_server_directory_path(ACCESS_DATABASE_PATH)

ACCESS_DATABASE = AccessDB(ACCESS_DATABASE_PATH)
