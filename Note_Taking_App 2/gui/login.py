import tkinter as tk
from tkinter import messagebox
from managers.manager import UserManager
from gui.register import RegisterScreen
from gui.note_screen import NoteScreen


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.user_manager = UserManager()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")

        self.username_entry.grid(row=0, column=1, padx=10)
        self.password_entry.grid(row=1, column=1, padx=10)

        login_button = tk.Button(self.root, text="Đăng nhập", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        register_button = tk.Button(self.root, text="Đăng ký", command=self.open_register)
        register_button.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user_manager.load_users()

        user = self.user_manager.get_user(username)
        if user and user.password == password:
            messagebox.showinfo("Thành công", f"Chào mừng {username}!")
            self.root.destroy()
            root = tk.Tk()
            NoteScreen(root, user)
            root.mainloop()

        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
       


    def open_register(self):
        register_window = tk.Toplevel(self.root)
        RegisterScreen(register_window)
