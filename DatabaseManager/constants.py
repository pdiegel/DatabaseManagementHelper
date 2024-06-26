import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from src.county_data_collectors.county_mapper import DATA_COLLECTOR_MAP

from DatabaseManager.models.access_database import AccessDB
from DatabaseManager.models.encryption_manager import EncryptionManager
from DatabaseManager.models.settings_manager import SettingsManager

# --- Titles and Labels ---
MAIN_TITLE = "Database Manager"

# --- Paths and Directories ---
logging.info("Setting up paths and directories.")
ROOT = Path(__file__).parent
DATA_DIRECTORY = ROOT / "data"
SERVER_DIRECTORY = Path("//server")
SERVER_ACCESS_DIRECTORY = SERVER_DIRECTORY / "access"
LOG_FILE_PATH = ROOT / "gui.log"
ENV_PATH = DATA_DIRECTORY / ".env"


# --- Environment Variables ---
ENV_VARIABLES = (
    "SENDER_EMAIL_ADDRESS",
    "SENDER_EMAIL_PASSWORD",
    "RECIPIENT_EMAIL_ADDRESS",
    "ENCRYPTION_KEY",
)


def load_env_vars() -> None:
    """This method will load the environment variables from the .env
    file.
    """
    if not ENV_PATH.exists():
        with open(ENV_PATH, "w") as file:
            for variable in ENV_VARIABLES:
                file.write(f"{variable}=\n")
            logging.info("Created .env file with empty variables.")
    # Override is set to True so that the environment variables can be
    # overwritten by the .env file if they already exist.
    load_dotenv(ENV_PATH, override=True)


try:
    load_env_vars()
    logging.info("Successfully loaded environment variables.")
except Exception as e:
    logging.error(f"Failed to load environment variables: {e}")


# --- Encryption and Settings ---
logging.info("Setting up encryption and settings.")


def get_encryption_manager() -> EncryptionManager:
    encryption_key_string = os.getenv("ENCRYPTION_KEY")
    if encryption_key_string:
        logging.info(
            f"Successfully got encryption key string: {encryption_key_string}"
        )
    return EncryptionManager(encryption_key_string)


try:
    ENCRYPTION_MANAGER = get_encryption_manager()
    logging.info("Successfully set up encryption manager.")
except Exception as e:
    logging.error(f"Failed to set up encryption manager: {e}")
    ENCRYPTION_KEY = None
else:
    ENCRYPTION_KEY = ENCRYPTION_MANAGER.key.decode()
    logging.info("Successfully decoded encryption key.")

SETTINGS_MANAGER = SettingsManager(ENV_PATH, ENCRYPTION_MANAGER)
logging.info("Successfully set up settings manager.")

logging.info("Saving encryption key to settings.")
SETTINGS_MANAGER.update_env_file("ENCRYPTION_KEY", ENCRYPTION_KEY)


# --- Utility Functions ---
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


def ensure_directory_exists(directory: Path) -> None:
    """This method will ensure that the directory exists. If the
    directory does not exist, it will be created.

    Args:
        directory (Path): The path to the directory.
    """
    if not directory.exists():
        directory.mkdir(parents=True)


# --- Data and Files ---
INTAKE_LABELS = DATA_DIRECTORY / "intake_labels.txt"
PARCEL_DATA_MAP = DATA_COLLECTOR_MAP
PARCEL_DATA_COUNTIES = list(PARCEL_DATA_MAP.keys())

# --- Access Database ---
ACCESS_DATABASE_PATH = (
    SERVER_ACCESS_DIRECTORY / "Database Backup" / "MainDB_be.accdb"
)
ACCESS_DATABASE_PATH = fix_server_directory_path(ACCESS_DATABASE_PATH)
ACCESS_DATABASE = AccessDB(ACCESS_DATABASE_PATH)

# --- Quotes Directory ---
QUOTES_DIRECTORY = SERVER_ACCESS_DIRECTORY / "quotes"
QUOTES_DIRECTORY = fix_server_directory_path(QUOTES_DIRECTORY)
ensure_directory_exists(QUOTES_DIRECTORY)
