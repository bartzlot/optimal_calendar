from lib import *

class EventList(QMainWindow):

    def __init__(self, parent = None):
        super(EventList, self).__init__(parent)
        uic.loadUi("holidays_list.ui", self)

        self.add_button = self.findChild(QPushButton, "add_button")
        self.del_button = self.findChild(QPushButton, "del_button")
        self.edit_button = self.findChild(QPushButton, "edit_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")
        self.holidays_list = self.findChild(QListWidget, "holidays_list")

