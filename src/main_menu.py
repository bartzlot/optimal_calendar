from lib import *

class MainMenu(QMainWindow):

    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("main_menu.ui"), self)
        self.calendar_button = self.findChild(QPushButton, "calendar_button")
        self.event_list_button = self.findChild(QPushButton, "event_list_button")
        self.options_button = self.findChild(QPushButton, "options_button")
        self.quit_button = self.findChild(QPushButton, "quit_button")

        self.db_manager = DatabaseManager()
        self.calendar = CalendarWindow(self.db_manager)
        self.list = EventList(self.db_manager, self.calendar)
        self.options = OptionsWindow(self.db_manager)

        self.options_button.clicked.connect(self.options_button_event)
        self.event_list_button.clicked.connect(self.event_list_button_event)
        self.calendar_button.clicked.connect(self.calendar_button_event)
        self.quit_button.clicked.connect(self.quit_button_event)

        self.list.database_updated.connect(self.calendar.updating_database)
        self.list.data_added.connect(self.calendar.mark_holidays_from_list)
        self.list.data_updated.connect(self.calendar.mark_holidays_from_list)
        self.list.data_deleted.connect(self.calendar.mark_holidays_from_list)


    def options_button_event(self):
        self.options.show()


    def calendar_button_event(self):
        self.calendar.show()


    def event_list_button_event(self):
        self.list.show()


    def quit_button_event(self):
        QApplication.quit()
    


app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())