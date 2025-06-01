import tkinter as tk
from tkinter import messagebox
from managers.manager import UserManager
from gui.admin_note_editor import AdminNoteEditor
class UserManagerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý người dùng")
        self.user_manager = UserManager()
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        self.users_listbox = tk.Listbox(self.root, width=50)
        self.users_listbox.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Thêm người dùng", command=self.add_user).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Xóa người dùng", command=self.delete_user).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Xem chi tiết", command=self.view_user).grid(row=0, column=2, padx=5)

    def load_users(self):
        self.users_listbox.delete(0, tk.END)
        self.users = self.user_manager.users
        for user in self.users:
            self.users_listbox.insert(tk.END, f"{user.username} - {user.role}")

    def add_user(self):
        win = tk.Toplevel(self.root)
        win.title("Thêm người dùng")

        tk.Label(win, text="Username:").pack()
        username_entry = tk.Entry(win)
        username_entry.pack()

        tk.Label(win, text="Password:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        tk.Label(win, text="Role (user/admin):").pack()
        role_entry = tk.Entry(win)
        role_entry.pack()

        def save():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get().lower()

            if not username or not password or role not in ("user", "admin"):
                messagebox.showwarning("Lỗi", "Vui lòng nhập đúng thông tin, role phải là 'user' hoặc 'admin'.")
                return

            if self.user_manager.get_user(username):
                messagebox.showwarning("Lỗi", "Username đã tồn tại!")
                return

            from models.user import User
            new_user = User(username, password, role)
            self.user_manager.users.append(new_user)
            self.user_manager.save_users()
            self.load_users()
            win.destroy()

        tk.Button(win, text="Lưu", command=save).pack(pady=5)

    def delete_user(self):
        selected = self.users_listbox.curselection()
        if not selected:
            messagebox.showwarning("Lỗi", "Vui lòng chọn người dùng để xóa.")
            return
        user = self.users[selected[0]]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa người dùng '{user.username}' không?")
        if confirm:
            self.user_manager.users.remove(user)
            self.user_manager.save_users()
            self.load_users()

    def view_user(self):
        selected = self.users_listbox.curselection()
        if not selected:
            return
        user = self.users[selected[0]]

        win = tk.Toplevel(self.root)
        win.title(f"Thông tin người dùng - {user.username}")

        tk.Label(win, text=f"Username: {user.username}", font=("Arial", 12)).pack(pady=5)
        tk.Label(win, text=f"Role: {user.role}", font=("Arial", 10)).pack(pady=5)

        tk.Button(win, text="Xem/Sửa Ghi chú", command=lambda: self.manage_notes(user)).pack(pady=10)

    def manage_notes(self, user):
        note_win = tk.Toplevel(self.root)
        AdminNoteEditor(note_win, user)
