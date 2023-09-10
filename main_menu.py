from lib import *

class MainMenu(QMainWindow, DatabaseManager):

    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        uic.loadUi("main_menu.ui", self)
        self.calendar_button = self.findChild(QPushButton, "calendar_button")
        self.event_list_button = self.findChild(QPushButton, "event_list_button")
        self.options_button = self.findChild(QPushButton, "options_button")
        self.quit_button = self.findChild(QPushButton, "quit_button")


        self.event_list_button.clicked.connect(self.options_button_event)
        self.calendar_button.clicked.connect(self.calendar_button_event)
        self.quit_button.clicked.connect(self.quit_button_event)
    

    def calendar_button_event(self):
        self.calendar = CalendarWindow()
        self.calendar.show()


    def options_button_event(self):
        self.list = EventList()
        self.list.show()


    def quit_button_event(self):
        QApplication.quit()

app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())