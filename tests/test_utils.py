import unittest
from utils import encrypt_password, decrypt_password

class TestUtils(unittest.TestCase):
    
    def test_encrypt_decrypt_password(self):
        """Verificar que la contraseña se cifra y descifra correctamente"""
        password = "mysecretpassword"
        
        # Encriptar la contraseña
        encrypted = encrypt_password(password)
        
        # Asegurarse de que la contraseña cifrada no sea igual a la original
        self.assertNotEqual(password, encrypted)
        
        # Desencriptar la contraseña
        decrypted = decrypt_password(encrypted)
        
        # Asegurarse de que la contraseña descifrada sea igual a la original
        self.assertEqual(password, decrypted)

if __name__ == '__main__':
    unittest.main()
