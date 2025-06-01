class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"], data.get("role", "user"))
