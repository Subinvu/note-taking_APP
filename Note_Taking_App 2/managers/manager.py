import json
import os
import sys
from models.user import User
from tkinter import messagebox

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class UserManager:
    def __init__(self, file_path="data/users.json"):
        self.file_path = get_resource_path(file_path)
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            if not os.path.exists(self.file_path):
                self.users = []
                return
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.users = [User.from_dict(user) for user in data]
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Lỗi", f"Không thể đọc users.json: {e}")
            self.users = []

    def save_users(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([user.to_dict() for user in self.users], f, indent=4)
        except IOError as e:
            messagebox.showerror("Lỗi", f"Không thể lưu users.json: {e}")

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None