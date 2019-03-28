import unittest
from tests.test_userManager import test_UserManager
from tests.test_TestDatabase import test_TestDatabase
from tests.test_ProgressDatabase import tets_ProgressDatabase
from tests.test_Engine import test_Engine

if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_cases = [test_UserManager, test_TestDatabase, tets_ProgressDatabase, test_Engine]
        ##  [test_Engine]##[test_UserManager, test_TestDatabase, tets_ProgressDatabase, test_Engine] ## [test_TestDatabase]
    tests = [loader.loadTestsFromTestCase(i) for i in test_cases]
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner().run(suite)
