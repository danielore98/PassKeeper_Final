import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db, init_db
from models import User, Password
from utils import encrypt_password, decrypt_password
from sqlalchemy.orm import Session
import pyperclip

# Inicializar la base de datos
init_db()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Contraseñas")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")  # Fondo de la ventana
        self.session = None
        self.db: Session = next(get_db())  # Obtener la sesión de la base de datos
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()

        # Título de la pantalla (Encabezado)
        header = tk.Label(self.root, text="Gestión de Contraseñas", font=("Helvetica", 24, "bold"), bg="#3b5998", fg="white")
        header.pack(fill="x", pady=20)

        # Frame de inicio de sesión
        frame = tk.Frame(self.root, bg="#ffffff", relief="solid", bd=1)
        frame.pack(pady=20, padx=50, fill="x", expand=True)

        # Etiquetas y campos de entrada
        self.create_label_entry(frame, "Correo Electrónico:", "email", 30)
        self.create_label_entry(frame, "Contraseña:", "password", 30, True)

        # Botones de iniciar sesión y registrar
        self.create_button(frame, "Iniciar sesión", self.login, "#3b5998", "white")
        self.create_button(frame, "Registrar nuevo usuario", self.register, "#42b72a", "white")

    def create_label_entry(self, frame, label_text, entry_name, width, is_password=False):
        """Crear etiquetas y campos de entrada"""
        tk.Label(frame, text=label_text, font=("Helvetica", 14), bg="#ffffff", fg="#333").pack(pady=5, anchor="w")
        entry = tk.Entry(frame, width=width, font=("Helvetica", 12))
        if is_password:
            entry.config(show="*")
        entry.pack(pady=5)
        setattr(self, entry_name, entry)

    def create_button(self, frame, text, command, bg_color, fg_color):
        """Crear botones estilizados"""
        button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=fg_color, font=("Helvetica", 14), relief="flat")
        button.pack(pady=10, fill="x")

    def login(self):
        email = self.email.get()
        password = self.password.get()

        if not email or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        user = self.db.query(User).filter(User.email == email).first()
        if user and user.password == password:
            self.session = user.id
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def register(self):
        self.clear_screen()

        # Frame de registro
        frame = tk.Frame(self.root, bg="#ffffff", relief="solid", bd=1)
        frame.pack(pady=20, padx=50, fill="x", expand=True)

        # Etiquetas y campos de entrada para el registro
        self.create_label_entry(frame, "Correo Electrónico:", "register_email", 30)
        self.create_label_entry(frame, "Nombre de Usuario:", "register_username", 30)
        self.create_label_entry(frame, "Contraseña:", "register_password", 30, True)

        # Botón de registro
        self.create_button(frame, "Registrar", self.process_registration, "#42b72a", "white")

        # Botón para volver al login
        self.create_button(frame, "Volver al login", self.create_login_screen, "#f0f4f8", "#333")

    def process_registration(self):
        email = self.register_email.get()
        username = self.register_username.get()
        password = self.register_password.get()

        if not email or not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        # Verificar si el correo o el nombre de usuario ya están en uso
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            messagebox.showerror("Error", "Correo ya registrado")
            return

        new_user = User(email=email, username=username, password=password)
        self.db.add(new_user)
        self.db.commit()
        messagebox.showinfo("Registro", "Usuario registrado con éxito")
        self.create_login_screen()

    def show_main_menu(self):
        self.clear_screen()

        # Menú principal
        tk.Label(self.root, text="Menú Principal", font=("Helvetica", 18), bg="#ffffff", fg="#333").pack(pady=20)

        self.create_button(self.root, "Añadir Contraseña", self.add_password, "#3b5998", "white")
        self.create_button(self.root, "Ver Contraseñas", self.view_passwords, "#42b72a", "white")
        self.create_button(self.root, "Cerrar sesión", self.logout, "#f44336", "white")

    def add_password(self):
        if self.session is None:
            messagebox.showerror("Error", "No has iniciado sesión.")
            return

        # Crear ventana de añadir contraseña
        add_password_window = tk.Toplevel(self.root)
        add_password_window.title("Añadir Contraseña")

        # Formulario de contraseña
        self.create_label_entry(add_password_window, "Nombre de la Contraseña", "password_name", 40)
        self.create_label_entry(add_password_window, "Nombre de Usuario", "password_user", 40)
        self.create_label_entry(add_password_window, "Contraseña", "password_value", 40, True)
        self.create_label_entry(add_password_window, "Categoría", "category", 40)

        # Botón para guardar
        self.create_button(add_password_window, "Guardar Contraseña", self.save_password, "#42b72a", "white")

    def save_password(self):
        password_name = self.password_name.get()
        password_user = self.password_user.get()
        password_value = self.password_value.get()
        category = self.category.get()

        if not password_name or not password_user or not password_value or not category:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        encrypted_password = encrypt_password(password_value)

        # Guardar la contraseña en la base de datos
        user = self.db.query(User).filter(User.id == self.session).first()
        new_password = Password(name=password_name, username=password_user,
                                encrypted_password=encrypted_password,
                                category=category, owner=user)
        self.db.add(new_password)
        self.db.commit()
        messagebox.showinfo("Contraseña añadida", "Contraseña guardada exitosamente.")
        self.clear_screen()
        self.show_main_menu()

    def view_passwords(self):
        if self.session is None:
            messagebox.showerror("Error", "No has iniciado sesión.")
            return

        user = self.db.query(User).filter(User.id == self.session).first()
        if not user or not user.passwords:
            messagebox.showinfo("Sin contraseñas", "No tienes contraseñas guardadas.")
            return

        password_list_window = tk.Toplevel(self.root)
        password_list_window.title("Contraseñas Guardadas")

        tk.Label(password_list_window, text="Tus Contraseñas", font=("Helvetica", 14), bg="#f0f4f8", fg="#333").pack(pady=10)

        for password in user.passwords:
            frame = tk.Frame(password_list_window)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{password.name} - {password.username} - {password.category}",
                     font=("Helvetica", 12), bg="#ffffff", fg="#333").pack(side="left", padx=5)
            copy_button = tk.Button(frame, text="Copiar Contraseña", command=lambda p=password: self.copy_password(p),
                                    bg="#3b5998", fg="white", relief="flat")
            copy_button.pack(side="right")

    def copy_password(self, password):
        decrypted_password = decrypt_password(password.encrypted_password)
        pyperclip.copy(decrypted_password)
        messagebox.showinfo("Contraseña Copiada", "La contraseña ha sido copiada al portapapeles.")

    def logout(self):
        self.session = None
        self.create_login_screen()

# Crear la ventana principal
root = tk.Tk()
app = App(root)
root.mainloop()
