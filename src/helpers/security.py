import os
import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CryptographyMessage:
    def __init__(self):
        self.key = hashlib.sha256(os.environ.get('SECRET_KEY').encode()).digest()

    def encrypt(self, _message: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_data = pad(_message.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, _message: str) -> str:
        encrypted_data = base64.b64decode(_message)
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        return decrypted_data.decode('utf-8')
