from modules.userManagement import UserManagement
from modules.TestDatabase import TestDatabase
from modules.TestDatabase import ProgressDatabase


class Engine:
    def __init__(self):
        self._userManagement = UserManagement()
        self._test_db = TestDatabase()
        self._progress_db = ProgressDatabase()
        self._username = ''
        self._password = ''

    def auth_user(self, username, password):
        user_id = self._userManagement.valid_user(username, password)
        if user_id:
            self._username, self._password = username, password
            available_tests = self._test_db.get_available_tests()
            return available_tests ## list of sqlite3.rows "SELECT quiz_id, name, description FROM quizzes"

    def select_test(self, user_id, quiz_id):
        self._progress_db.return_progress(user_id, quiz_id)

    def select_mode(self, quantity = 20, exam = False):
        pass

