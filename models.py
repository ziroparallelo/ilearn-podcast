from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, type, username):
        self.id = id
        self.email = email
        self.password = password
        self.type = type
        self.username = username
        