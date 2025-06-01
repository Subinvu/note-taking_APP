import json
import os
import sys
from models.note import Note
from tkinter import messagebox

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class NoteManager:
    def __init__(self, file_path="data/notes.json"):
        self.file_path = get_resource_path(file_path)
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            if not os.path.exists(self.file_path):
                self.notes = []
                return
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.notes = [Note.from_dict(n) for n in data]
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Lỗi", f"Không thể đọc notes.json: {e}")
            self.notes = []

    def save_notes(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([n.to_dict() for n in self.notes], f, indent=4)
        except IOError as e:
            messagebox.showerror("Lỗi", f"Không thể lưu notes.json: {e}")

    def get_notes_by_user(self, username):
        return [n for n in self.notes if n.username == username]

    def add_note(self, title, content, username):
        note_id = max([n.id for n in self.notes], default=0) + 1
        new_note = Note(note_id, title, content, username)
        self.notes.append(new_note)
        self.save_notes()

    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n.id != note_id]
        self.save_notes()

    def update_note(self, note_id, new_title, new_content):
        for note in self.notes:
            if note.id == note_id:
                note.title = new_title
                note.content = new_content
                break
        self.save_notes()