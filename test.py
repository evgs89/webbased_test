import unittest
from tests.test_userManager import test_UserManager
from tests.test_TestDatabase import test_TestDatabase
from tests.test_ProgressDatabase import tets_ProgressDatabase

if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_cases = [test_UserManager, test_TestDatabase, tets_ProgressDatabase]
    tests = [loader.loadTestsFromTestCase(i) for i in test_cases]
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner().run(suite)
