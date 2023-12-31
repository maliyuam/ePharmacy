# TODO: Nothing -:

class User:
    def __init__(self, username: str, fullname: str, role: str, logged_in: bool) -> None:
        self.username = username
        self.fullname = fullname
        self.role = role
        self.logged_in = logged_in
    # create the tostring method

    def __str__(self) -> str:
        return f"{self.username:^20} | {self.fullname:^20} | {self.role:^20} | {self.logged_in:^20}"

    # create the repr method

    def __repr__(self) -> str:
        return f"{self.username} {self.fullname} {self.role} {self.logged_in}"
