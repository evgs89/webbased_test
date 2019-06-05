from modules.console_quizz import TestApp
from modules.importer import SpecialFileImporter
from modules.TestDatabase import TestDatabase

if __name__ == "__main__":
    # fi = SpecialFileImporter()
    # questions = fi.open_file("med_test_orig.txt")
    # td = TestDatabase()
    # td.save_to_db_file('medtest.db', questions, replace = True)
    #
    # td = TestDatabase()
    # description = 'аккредитация 1 этап 34.02.01 СЕСТРИНСКОЕ ДЕЛО'
    # td.load_to_db(td.load_from_db_file('medtest.db').values(), 'Гинекология', description)

    main_test = TestApp()
    main_test.run()
