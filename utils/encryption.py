import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_salt() -> bytes:
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encode_salt(salt: bytes) -> str:
    return base64.b64encode(salt).decode()

def decode_salt(salt_str: str) -> bytes:
    return base64.b64decode(salt_str)

def encrypt_text(text, key):
    fernet = Fernet(key)
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_text.encode()).decode()
