import os
import base64
import hashlib

from flask import abort, request
from flask_httpauth import HTTPBasicAuth

from Crypto.Cipher import AES  # nosec
from Crypto.Util.Padding import pad, unpad  # nosec

auth = auth = HTTPBasicAuth()


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


@auth.verify_password
def verify_password(_username: str, _password: str):
    header = request.authorization

    if not header:
        return abort(401, 'Missing Authorization Header')

    if not check_auth(_username, _password):
        return abort(401, 'The invalid token')

    return True


def check_auth(_username: str, _password: str):
    _security_field = CryptographyMessage()

    username = _security_field.encrypt(os.environ.get('AUTH_USERNAME'))
    password = _security_field.encrypt(os.environ.get('AUTH_PASSWORD'))

    result = username == _username and password == _password

    return result
