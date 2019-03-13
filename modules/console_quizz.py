import npyscreen
from modules.quiz_engine import Engine



class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self._engine = Engine()
        self._availableTests = []
        self.addForm('LOGIN', LoginForm)
        self.addForm('LOGIN_ERROR', LoginErrorForm)
        self.addForm('SELECT_TEST', SelectTestForm)
        self.addForm('SELECT_MODE', SelectModeForm)



class LoginForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.FixedText(value = "Please input your username and password"))
        self._login = self.add(npyscreen.TitleText(name = "Username: "))
        self._password = self.add(npyscreen.TitlePassword(name = "Password: "))
        self.nextrely += 1
        self.add(npyscreen.FixedText(value = 'For exiting app press Ctrl+C'))

    def afterEditing(self):
        listTests = self.parentApp._engine.validateUser(self._login, self._password)
        if listTests:
            self.parentApp._availableTests = listTests
            self.parentApp.setNextForm('SELECT_TEST')
        else: self.parentApp.setNextForm('LOGIN_ERROR')


class LoginErrorForm(npyscreen.fmPopup.Popup):
    def create(self):
        self.add(npyscreen.FixedText(value = "Login error. Username and/or password incorrect."))

    def afterEditing(self):
        self.parentApp.setNextForm('LOGIN')

class SelectTestForm(npyscreen.Form):
    def create(self):
        for test in self.parentApp._availableTests:



class SelectModeForm(npyscreen.Form):
    def create(self):
        pass


class TestForm(npyscreen.Form):
    def create(self):
        pass

    def afterEditing(self):
        "validate user's answer and set next form"


class ResultForm(npyscreen.Form):
    def create(self):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)