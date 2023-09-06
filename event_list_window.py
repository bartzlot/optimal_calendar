from lib import *

class EventList(QMainWindow):

    def __init__(self, parent = None):
        super(EventList, self).__init__(parent)
        uic.loadUi("holidays_list.ui", self)

        self.add_button = self.findChild(QPushButton, "add_button")
        self.del_button = self.findChild(QPushButton, "del_button")
        self.edit_button = self.findChild(QPushButton, "edit_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")
        self.holidays_list = self.findChild(QTableWidget, "holidays_list")
        self.creating_table()
        self.inserting_dict_to_list(DatabaseManager.getting_data_excel(DatabaseManager, 'polish_database.xlsx'))

    def creating_table(self):
        self.holidays_list.insertColumn(0)
        self.holidays_list.insertColumn(1)
        self.holidays_list.setHorizontalHeaderLabels(('Day description', 'Date'))
        self.holidays_list.setColumnWidth(0, 450)
        self.holidays_list.setColumnWidth(1, 130)


    def inserting_dict_to_list(self, data: dict):
        for index, records in enumerate(data):
            self.holidays_list.insertRow(index)
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(records['DATE'].toString("yyyy.MM.dd")))
        

    def add_button_event(self): #TODO
        add_action = DateEdit() 


class DateEdit(QDialog): #TODO
    def __init__(self, parent = None):
        super(DateEdit, self).__init__(parent)
        uic.loadUi("date_insertion.ui", self)
        
        self.day_description_input = self.findChild(QTextEdit, "day_desc_textedit")
        self.date_input = self.findChild(QTextEdit, "date_texedit")
        self.dialog_options = self.findChild(QDialogButtonBox, "buttonbox")

    
    def adding_new_date(self):
        pass


    def deleting_date(self):
        pass


    def editing_date(self):
        pass


    
app = QApplication(sys.argv)
window = DateEdit()
window.show()
sys.exit(app.exec())    


