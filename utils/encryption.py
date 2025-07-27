from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_text(plain_text):
    key = load_key()
    f = Fernet(key)
    token = f.encrypt(plain_text.encode()).decode()
    return "enc:" + token

def decrypt_text(encrypted_text):
    if not encrypted_text.startswith("enc:"):
        return encrypted_text
    key = load_key()
    f = Fernet(key)
    token = encrypted_text[4:]
    return f.decrypt(token.encode()).decode()

