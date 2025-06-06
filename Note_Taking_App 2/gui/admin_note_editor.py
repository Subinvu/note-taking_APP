import tkinter as tk
from tkinter import messagebox
from managers.note_manager import NoteManager

class AdminNoteEditor:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"Ghi chú của người dùng: {user.username}")
        self.user = user
        self.note_manager = NoteManager()
        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        tk.Label(self.root, text=f"Ghi chú của {self.user.username}", font=("Arial", 14)).pack(pady=10)

        self.notes_listbox = tk.Listbox(self.root, width=50)
        self.notes_listbox.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Xem", command=self.view_note).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sửa", command=self.edit_note).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.delete_note).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Thêm", command=self.add_note).grid(row=0, column=3, padx=5)

    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)
        self.notes = self.note_manager.get_notes_by_user(self.user.username)
        for note in self.notes:
            self.notes_listbox.insert(tk.END, f"{note.id} - {note.title}")

    def view_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            return
        note = self.notes[selected[0]]

        win = tk.Toplevel(self.root)
        win.title(note.title)

        tk.Label(win, text=note.title, font=("Arial", 12, "bold")).pack(pady=5)
        tk.Message(win, text=note.content, width=400).pack(padx=10, pady=5)

    def edit_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            return
        note = self.notes[selected[0]]

        win = tk.Toplevel(self.root)
        win.title("Sửa ghi chú")

        tk.Label(win, text="Tiêu đề:").pack()
        title_entry = tk.Entry(win)
        title_entry.insert(0, note.title)
        title_entry.pack()

        tk.Label(win, text="Nội dung:").pack()
        content_text = tk.Text(win, height=10, width=40)
        content_text.insert("1.0", note.content)
        content_text.pack()

        def save():
            new_title = title_entry.get()
            new_content = content_text.get("1.0", tk.END).strip()
            if not new_title or not new_content:
                messagebox.showwarning("Lỗi", "Không được để trống")
                return
            note.title = new_title
            note.content = new_content
            self.note_manager.save_notes()
            self.load_notes()
            win.destroy()

        tk.Button(win, text="Lưu", command=save).pack(pady=5)

    def delete_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            return
        note = self.notes[selected[0]]
        confirm = messagebox.askyesno("Xác nhận", f"Xóa ghi chú '{note.title}'?")
        if confirm:
            self.note_manager.delete_note(note.id)
            self.load_notes()
    
    def add_note(self):
        win = tk.Toplevel(self.root)
        win.title(f"Thêm ghi chú cho {self.user.username}")

        tk.Label(win, text="Tiêu đề:").pack()
        title_entry = tk.Entry(win)
        title_entry.pack()

        tk.Label(win, text="Nội dung:").pack()
        content_text = tk.Text(win, height=10, width=40)
        content_text.pack()

        def save():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if not title or not content:
                messagebox.showwarning("Lỗi", "Không được để trống")
                return
            self.note_manager.add_note(title, content, self.user.username)
            self.load_notes()
            win.destroy()

        tk.Button(win, text="Lưu", command=save).pack(pady=5)
