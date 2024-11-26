from cryptography.fernet import Fernet
from config import KEY_FILE
import os

# Generar una clave de cifrado
def generate_key():
    return Fernet.generate_key()

# Obtener el cifrador (Fernet) con la clave
def get_cipher():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            key = file.read()
    else:
        key = generate_key()
        with open(KEY_FILE, 'wb') as file:
            file.write(key)
    return Fernet(key)

# Encriptar una contraseña
def encrypt_password(password):
    cipher = get_cipher()
    return cipher.encrypt(password.encode()).decode()

# Desencriptar una contraseña
def decrypt_password(encrypted_password):
    cipher = get_cipher()
    return cipher.decrypt(encrypted_password.encode()).decode()
