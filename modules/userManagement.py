import sqlite3
import os
import hashlib
import random, string


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def hash_password(password):
    return hashlib.md5(bytes(password, encoding = 'utf8')).hexdigest()


class UserManagement:
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

    def _is_user(self, name):
        conn, cur = self._connect_db()
        cur.execute("SELECT user_id FROM users WHERE username = ?", name)
        if cur.fetchall(): return True
        else: return False

    def create_user(self, name):
        conn, cur = self._connect_db()
        if self._is_user(name):
            print('This username is already in use! Select another one!')
            return False
        else:
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (id_generator(10), name, hash_password(''), ''))
            conn.commit()
            return True


    def change_password(self, name, old_password, new_password):
        "default password is empty string - '' "
        conn, cur = self._connect_db()



    def delete_user(self, name):
        pass




