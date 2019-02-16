import sqlite3
import os
import random


class UserManagement:
    def __init__(self):
        self._db_file = 'databases/users.db'
        if not os.path.isfile(self._db_file):
            conn = sqlite3.connect(self._db_file)
            cur = conn.cursor()
            cur.execute("CREATE TABLE users (user_id TEXT, username TEXT, pass_hash TEXT, last_login TEXT)")
            conn.commit()

    def create_user(self, name):
        pass

    def change_password(self, name, old_password, new_password):
        "default password is empty string - '' "
        pass

    def delete_user(self, name):
        pass


