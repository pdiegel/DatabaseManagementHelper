from cryptography.fernet import Fernet
from typing import Union
import logging


class EncryptionManager:
    """Manages encryption and decryption of passwords."""

    def __init__(self, key: Union[str, bytes] = None):
        if key:
            key = key.encode()

            if len(key) != 44:
                raise ValueError(
                    "The encryption key must be 44 characters long."
                )
            self.key = key

        else:
            self.key = Fernet.generate_key()
            # This key is already in the correct format
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts the text using the cipher_suite object.

        Args:
            plaintext (str): The plaintext password string.

        Returns:
            bytes: The encrypted password.
        """
        try:
            return self.cipher_suite.encrypt(plaintext.encode())
        except Exception as e:
            logging.error(f"Error encrypting password: {e}", exc_info=True)

    def decrypt(self, ciphertext: Union[str, bytes]) -> str:
        """Decrypts the text using the cipher_suite object.

        Args:
            ciphertext (str): The encrypted password string.

        Returns:
            str: The decrypted password.
        """
        try:
            return self.cipher_suite.decrypt(ciphertext)
        except Exception as e:
            logging.error(f"Error decrypting password: {e}", exc_info=True)
        return ""
