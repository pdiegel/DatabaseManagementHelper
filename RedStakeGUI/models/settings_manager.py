import logging
import os
from pathlib import Path
from typing import Tuple

from RedStakeGUI.models.encryption_manager import EncryptionManager


class SettingsManager:
    """Manages the settings for the RedStake GUI."""

    def __init__(
        self,
        env_path: Path,
        encryption_manager: EncryptionManager,
    ):
        self.env_path = env_path
        self.encryption_manager = encryption_manager

    def save_email_settings(
        self,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
    ) -> None:
        """Saves the email settings to the .env file.

        Args:
            sender_email (str): The sender email address.
            sender_password (str): The sender email password.
            recipient_email (str): The recipient email address.
        """
        # Encrypt the password
        logging.debug(f"Encrypting password on save: {sender_password}")
        encrypted_password = self.encryption_manager.encrypt(sender_password)
        logging.debug(f"Encrypted password on save: {encrypted_password}")

        variables = {
            "SENDER_EMAIL_ADDRESS": sender_email,
            "SENDER_EMAIL_PASSWORD": encrypted_password.decode(),
            "RECIPIENT_EMAIL_ADDRESS": recipient_email,
        }
        for variable, value in variables.items():
            try:
                logging.debug(f"Updating {variable} to {value}")
                self.update_env_file(variable, value)
            except Exception as e:
                logging.error(f"Error updating {variable} on save: {e}")

    def get_email_settings(self) -> Tuple[str, str, str]:
        """Returns the email environmental variables.

        Returns:
            Tuple[str, str, str]: The sender email address, recipient
                email address, and sender email password.
        """
        sender_email = os.getenv("SENDER_EMAIL_ADDRESS")
        recipient_email = os.getenv("RECIPIENT_EMAIL_ADDRESS")
        encrypted_password = os.getenv("SENDER_EMAIL_PASSWORD")
        password = ""

        # Error handling for corrupted settings file
        try:
            password = self.encryption_manager.decrypt(encrypted_password)
        except Exception as e:
            logging.error(f"Error decrypting password: {e}")
        finally:
            return sender_email, recipient_email, password

    def update_env_file(
        self,
        key: str,
        value: str,
    ) -> None:
        """Updates a key-value pair in the .env file.

        Args:
            key (str): The key to update.
            value (str): The value to update.
        """
        lines = []
        found = False
        if self.env_path.exists():
            with open(self.env_path, "r") as file:
                lines = file.readlines()

            # Update the value if key exists
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    found = True
                    break

        # Append the key-value pair if key doesn't exist
        if not found:
            lines.append(f"{key}={value}\n")

        # Write back to file
        with open(self.env_path, "w") as file:
            file.writelines(lines)
