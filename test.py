import unittest
from tests.test_userManagement import test_UserManagement


if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_cases = [test_UserManagement, ]
    tests = [loader.loadTestsFromTestCase(i) for i in test_cases]
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner().run(suite)
