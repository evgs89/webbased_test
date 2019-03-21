import sqlite3
import os
from modules.my_functions import hash_password, id_generator
from modules.TestDatabase import ProgressDatabase


class DuplicateUsernameException(Exception):
    def __init__(self, *args):
        pass


class UserManager:
    def __init__(self):
        self._db_file = 'databases/users.db'
        if not os.path.isfile(self._db_file):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE users (user_id TEXT, username TEXT, pass_hash TEXT, last_login TEXT)")
            conn.commit()

    def _connect_db(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        return [conn, cur]

    def get_user_id(self, name):
        conn, cur = self._connect_db()
        cur.execute("SELECT user_id FROM users WHERE username = ?", (name, ))
        id = cur.fetchone()
        if id: id = id[0]
        return id

    def valid_user(self, username, password):
        conn, cur = self._connect_db()
        cur.execute("SELECT user_id FROM users WHERE username = ? AND pass_hash = ?", (username, hash_password(password)))
        user_id = cur.fetchone()
        if user_id: user_id = user_id[0]
        return user_id

    def create_user(self, name):
        conn, cur = self._connect_db()
        if self.get_user_id(name): raise DuplicateUsernameException(name)
        else:
            user_id = id_generator(10)
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, name, hash_password(''), ''))
            conn.commit()
            pd = ProgressDatabase(self)
            pd.create_user(user_id)
            return user_id

    def change_password(self, name, old_password, new_password):
        conn, cur = self._connect_db()
        cur.execute("UPDATE users SET pass_hash = ? WHERE username = ? AND pass_hash = ?", (hash_password(new_password),
                                                                                            name,
                                                                                            hash_password(old_password)))
        conn.commit()
        if cur.rowcount < 1:
            print("Name or password mismatch")
        else:
            return True

    def delete_user(self, name):
        conn, cur = self._connect_db()
        cur.execute("SELECT user_id FROM users WHERE username = ?", (name, ))
        user_row = cur.fetchone()
        if user_row:
            user_id = user_row[0]
            cur.execute("DELETE FROM users WHERE username = ?", (name, ))
            conn.commit()
            ProgressDatabase(self).delete_user(user_id)
        else:
            print('No such user')
            return True
        return cur.rowcount > 0

    def get_list_of_users(self):
        conn, cur = self._connect_db()
        cur.execute("SELECT user_id, username FROM users")
        return cur.fetchall()

