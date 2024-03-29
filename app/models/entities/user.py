from werkzeug.security import check_password_hash, generate_password_hash


class User():

    def __init__(self, id, user, password) -> None:
        self.id = id
        self.user = user
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

# print(generate_password_hash("12345"))
