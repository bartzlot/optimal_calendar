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

        self.database = DatabaseManager.getting_data_excel(DatabaseManager, 'polish_database.xlsx')

        self.creating_table()
        self.inserting_dict_to_list()

        self.add_button.clicked.connect(self.add_button_event)
        self.edit_button.clicked.connect(self.edit_button_event)




    def creating_table(self):
        self.holidays_list.insertColumn(0)
        self.holidays_list.insertColumn(1)
        self.holidays_list.setHorizontalHeaderLabels(('Day description', 'Date'))
        self.holidays_list.setColumnWidth(0, 450)
        self.holidays_list.setColumnWidth(1, 130)


    def inserting_dict_to_list(self):
        for index, records in enumerate(self.database):
            self.holidays_list.insertRow(index)
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(records['DATE'].toString("dd.MM.yyyy")))
        

    def add_button_event(self): #TODO
        add_action = DateEdit(self)
        new_date = add_action.adding_new_date()
        print(new_date)


    def edit_button_event(self):
        edit_action = DateEdit(self)
        
        selected_rows = set()
        selected_items = self.holidays_list.selectedItems()

        for item in selected_items:
            selected_rows.add(item.row())
        
        for data in selected_rows:
            new_date = edit_action.editing_date(self.database[data]['DAY_DESC'], self.database[data]['DATE'])
            print(new_date)

        


class DateEdit(QDialog): #TODO
    def __init__(self, parent = EventList):
        super(DateEdit, self).__init__(parent)
        uic.loadUi("date_insertion.ui", self)
        
        self.day_description_input = self.findChild(QTextEdit, "day_desc_textedit")
        self.date_input = self.findChild(QDateEdit, "dateEdit")
        self.dialog_options = self.findChild(QDialogButtonBox, "buttonBox")
        self.dialog_options.accepted.connect(self.accept) 
        self.dialog_options.rejected.connect(self.reject) 
        
    def adding_new_date(self):
        self.date_input.setDateTime(QDateTime.currentDateTime())
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            edited_date = {'DATE_DESC': self.day_description_input.toPlainText(),
                           'DATE': self.date_input.date()}
            return edited_date
        else:
            return None


    def deleting_date(self):
        print('sads')
        pass


    def editing_date(self, day_description: str, days_date: QDate):
        
        self.date_input.setDate(days_date)
        self.day_description_input.setText(day_description)
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            edited_date = {'DATE_DESC': self.day_description_input.toPlainText(),
                           'DATE': self.date_input.date()}
            return edited_date
        else:
            return None

# app = QApplication(sys.argv)
# window = DateEdit()
# window.show()
# sys.exit(app.exec())    


