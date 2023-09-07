from cryptography.fernet import Fernet
import base64
from typing import Union
import logging
import hashlib


class EncryptionManager:
    """Manages encryption and decryption of passwords."""

    def __init__(self, key: Union[str, bytes] = None):
        if key:
            print(f"Key: {key}")
            print(f"Encoded key: {key.encode()}")
            self.key = base64.urlsafe_b64encode(key.encode())
            print(f"B64 encoded key: {self.key}")
            print(f"Key length: {len(self.key)}")
            print(f"Key type: {type(self.key)}")
            if len(self.key) != 32:
                raise ValueError("Invalid key length")
        else:
            self.key = Fernet.generate_key()
            print(f"Fernet key: {self.key}")
            print(f"Fernet key length: {len(self.key)}")
            print(f"Fernet key type: {type(self.key)}")
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
            return self.cipher_suite.encrypt(
                self.convert_string_to_bytes(plaintext)
            )
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
            decoded_value = self.convert_string_to_bytes(ciphertext)
        except Exception as e:
            logging.error(f"Error decoding password: {e}", exc_info=True)
            return ""

        try:
            return self.cipher_suite.decrypt(decoded_value).decode()
        except Exception as e:
            logging.error(f"Error decrypting password: {e}", exc_info=True)
        return ""

    def convert_bytes_to_string(self, byte_like: bytes) -> str:
        """Converts bytes to a string.

        Args:
            byte_like (bytes): The bytes to convert.

        Returns:
            str: The converted string.
        """
        return base64.urlsafe_b64encode(byte_like).decode()

    def convert_string_to_bytes(self, string: str) -> bytes:
        """Converts a string to bytes.

        Args:
            string (str): The string to convert.

        Returns:
            bytes: The converted bytes.
        """
        return base64.urlsafe_b64decode(string.encode())
