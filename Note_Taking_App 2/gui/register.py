import tkinter as tk
from tkinter import messagebox
from managers.manager import UserManager
from models.user import User

class RegisterScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng ký")
        self.user_manager = UserManager()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Xác nhận Password:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Vai trò:").grid(row=3, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        self.confirm_entry = tk.Entry(self.root, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.confirm_entry.grid(row=2, column=1)

        self.role_var = tk.StringVar(value="user")
        tk.OptionMenu(self.root, self.role_var, "user", "admin").grid(row=3, column=1)

        tk.Button(self.root, text="Đăng ký", command=self.register).grid(row=4, column=0, columnspan=2, pady=10)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Không được để trống!")
            return

        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
            return

        if self.user_manager.get_user(username):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
            return

        new_user = User(username, password, role)
        self.user_manager.users.append(new_user)
        self.user_manager.save_users()
        messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
        self.root.destroy()  # Đóng form đăng ký
