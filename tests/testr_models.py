import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Password
from utils import encrypt_password, decrypt_password

# Crear una base de datos en memoria para pruebas
SQLITE_URL = "sqlite:///:memory:"

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración de la base de datos para las pruebas"""
        cls.engine = create_engine(SQLITE_URL, echo=True)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    def setUp(self):
        """Limpiar la base de datos antes de cada prueba"""
        self.session.query(User).delete()
        self.session.query(Password).delete()
        self.session.commit()

    def test_user_creation(self):
        """Probar la creación de un usuario"""
        new_user = User(email="testuser@example.com", username="testuser", password="password123")
        self.session.add(new_user)
        self.session.commit()
        user = self.session.query(User).filter(User.email == "testuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "testuser@example.com")

    def test_password_encryption(self):
        """Probar el cifrado de contraseñas"""
        password_value = "mysecretpassword"
        encrypted_password = encrypt_password(password_value)
        self.assertNotEqual(password_value, encrypted_password)
        decrypted_password = decrypt_password(encrypted_password)
        self.assertEqual(password_value, decrypted_password)

    def test_add_password(self):
        """Probar la creación de una contraseña asociada a un usuario"""
        new_user = User(email="user@example.com", username="user", password="password123")
        self.session.add(new_user)
        self.session.commit()

        user = self.session.query(User).filter(User.email == "user@example.com").first()
        new_password = Password(name="Google", username="user_google", encrypted_password=encrypt_password("googlepassword"), category="Social", owner=user)
        self.session.add(new_password)
        self.session.commit()

        password = self.session.query(Password).filter(Password.name == "Google").first()
        self.assertIsNotNone(password)
        self.assertEqual(password.name, "Google")
        self.assertEqual(password.category, "Social")

    @classmethod
    def tearDownClass(cls):
        """Limpiar la base de datos después de las pruebas"""
        cls.session.close()
        cls.engine.dispose()

if __name__ == '__main__':
    unittest.main()
