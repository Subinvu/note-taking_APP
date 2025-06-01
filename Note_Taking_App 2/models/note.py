class Note:
    def __init__(self, note_id, title, content, username):
        self.id = note_id
        self.title = title
        self.content = content
        self.username = username

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "username": self.username
        }

    @staticmethod
    def from_dict(data):
        return Note(data["id"], data["title"], data["content"], data["username"])