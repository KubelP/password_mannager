'''Module Cryptografer responsible for hashing password in both ways'''
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Cryptografer:
    '''Crytografter contains methodes used for crypting (encode) and decrypting (decode) text, takes arguments \
    password: bytes, salt: bytes, text: bytes'''
    def __init__(self, password: bytes, salt: bytes, text: bytes) -> None:
        self.password = password
        self.salt = salt
        self.text = text
        self.fernet = None

    def kdf(self):
        '''main encoding methode'''
        kdf = PBKDF2HMAC (algorithm= hashes.SHA256(),
        length= 32,
        salt = self.salt,
        iterations= 390000)
        fernet_input = base64.urlsafe_b64encode(kdf.derive(self.password))
        self.fernet = Fernet(fernet_input)
        return self.fernet

    def encrypt(self):
        '''encryption'''
        return self.fernet.encrypt(self.text)

    def decrypt(self):
        '''decryption'''
        return self.fernet.decrypt(self.text)
