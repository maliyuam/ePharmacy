from __future__ import annotations

from .user import User
from typing import List
import os


class UserManagement:
    """Main class to manage the user accounts

    Attributes:
        users: A list of users
        status_file: file where log ins are recorded
    """

    def __init__(self, status_file: str = 'data/.logged_in', users: List[User] = []) -> None:
        self.users = users
        self.status_file = status_file

    def get_logged_in_user(self) -> User:
        if(not os.path.exists(self.status_file)):
            raise FileNotFoundError("File does not exist")
        with open(self.status_file, 'r') as f:
            username = f.read().strip()

            user = self.get_user_details(username)
            if user is None:
                raise Exception("User is not logged in")
            if user.logged_in is False:
                raise Exception("User is not logged in")
            return user

    def get_user_details(self, username: str) -> User:
        """Returns the account of a user
        Args:
            username: the target username
        """
        for user in self.users:
            if user.username == username:
                return user

    @staticmethod
    def load(infile: str = '') -> UserManagement:
        """Loads the accounts from a file"""
        # open the file and retrieve the relevant fields to create the objects.
        with open(infile, 'r') as f:

            users = [User(elements[0], elements[3], elements[4], True if (elements[5] == "1" or elements[5] == 1) else False)
                     for line in f.readlines() if (elements := line.strip().split(':'))]
            current_folder = os.path.dirname(os.path.abspath(__file__))
            data_folder = os.path.abspath(
                os.path.join(current_folder, '../../data'))
            login_creds = os.path.join(data_folder, '.logged_in')
            return UserManagement(users=users, status_file=login_creds)
