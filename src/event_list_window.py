from PyQt6 import QtGui
from lib import *

class EventList(QMainWindow):
    data_added = pyqtSignal(list)
    data_updated = pyqtSignal(list)
    data_deleted = pyqtSignal(list)
    database_updated = pyqtSignal(list)
    def __init__(self, db_manager, calendar, parent = None):
        super(EventList, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("holidays_list.ui"), self)

        self.add_button = self.findChild(QPushButton, "add_button")
        self.multiple_add_button = self.findChild(QPushButton, "multiple_add_button")
        self.del_button = self.findChild(QPushButton, "del_button")
        self.edit_button = self.findChild(QPushButton, "edit_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")
        self.holidays_list = self.findChild(QTableWidget, "holidays_list")
        self.db_manager = db_manager
        self.database = db_manager.getting_data_excel('polish_database.xlsx')
        self.calendar_window_instance = calendar

        self.creating_table()
        self.inserting_data_to_list()

        self.add_button.clicked.connect(self.add_button_event)
        self.multiple_add_button.clicked.connect(self.multiple_add_button_event)
        self.edit_button.clicked.connect(self.edit_button_event)
        self.exit_button.clicked.connect(self.exit_button_event)
        self.del_button.clicked.connect(self.delete_button_event)


    def creating_table(self):
        self.holidays_list.insertColumn(0)
        self.holidays_list.insertColumn(1)
        self.holidays_list.insertColumn(2)
        self.holidays_list.setHorizontalHeaderLabels(('Day description', 'Date', 'Day type'))
        self.holidays_list.setColumnWidth(0, 350)
        self.holidays_list.setColumnWidth(1, 105)
        self.holidays_list.setColumnWidth(2, 105)


    def inserting_data_to_list(self):
        for index, records in enumerate(self.database):
            temp_date_in_str = records['DATE'].toString("dd.MM.yyyy")
            self.holidays_list.insertRow(index)
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(temp_date_in_str))
            self.holidays_list.setItem(index, 2, QTableWidgetItem(records['TYPE']))


    def updating_list(self):
        for index, records in enumerate(self.database):
            temp_date_in_str = records['DATE'].toString("dd.MM.yyyy")
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(temp_date_in_str))
            self.holidays_list.setItem(index, 2, QTableWidgetItem(records['TYPE']))


    def add_button_event(self):
        add_action = DateEdit(self)
        new_date = add_action.adding_new_date()

        if new_date is not None:
            self.database = self.db_manager.sorting_database(self.database, new_date)
            self.dates_list = self.db_manager.extracting_dates(self.database)
            self.updating_list()
            self.data_added.emit(self.dates_list)
            self.database_updated.emit(self.database)
        else: pass
    

    def multiple_add_button_event(self):
        add_multiple_action = MultipleDateEdit(self)
        new_dates_list = add_multiple_action.adding_new_date_range()

        if new_dates_list is not None:
            for date in new_dates_list:
                self.database = self.db_manager.sorting_database(self.database, date)

            self.dates_list = self.db_manager.extracting_dates(self.database)       
            self.updating_list()
            self.data_added.emit(self.dates_list)
            self.database_updated.emit(self.database)
        else: pass
        

    def edit_button_event(self):
        edit_action = DateEdit(self)
        new_date = []
        selected_rows = set()
        selected_items = self.holidays_list.selectedItems()

        for item in selected_items:
            selected_rows.add(item.row())
        
        for data in selected_rows:
            new_date = edit_action.editing_date(self.database[data]['DAY_DESC'], self.database[data]['TYPE'], self.database[data]['DATE'])
            if new_date is not None:
                self.database = self.db_manager.editing_database(self.database, new_date, data)
            else:
                continue
        self.updating_list()
        self.dates_list = self.db_manager.extracting_dates(self.database)
        self.data_updated.emit(self.dates_list)
        self.database_updated.emit(self.database)
        DatabaseManager.saving_data_to_excel(DatabaseManager, self.database, 'polish_database.xlsx')

    def delete_button_event(self):
        selected_rows = set()
        selected_items = self.holidays_list.selectedItems()

        for item in selected_items:
            selected_rows.add(item.row())
        self.database = self.db_manager.deleting_records(self.database, selected_rows)
        self.updating_list()
        self.dates_list = self.db_manager.extracting_dates(self.database)
        self.data_updated.emit(self.dates_list)
        self.database_updated.emit(self.database)

    def exit_button_event(self):
        self.close()
        


class DateEdit(QDialog):
    def __init__(self, parent = EventList):
        super(DateEdit, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("date_insertion.ui"), self)
        
        self.day_description_input = self.findChild(QTextEdit, "day_desc_textedit")
        self.day_type_input = self.findChild(QTextEdit, "day_type_textedit")
        self.date_input = self.findChild(QDateEdit, "dateEdit")
        self.dialog_options = self.findChild(QDialogButtonBox, "buttonBox")
        self.dialog_options.accepted.connect(self.accept) 
        self.dialog_options.rejected.connect(self.reject) 
        
    def adding_new_date(self):
        self.date_input.setDateTime(QDateTime.currentDateTime())
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            edited_date = {'DAY_DESC': self.day_description_input.toPlainText(),
                           'DATE': self.date_input.date(),
                           'TYPE': self.day_type_input.toPlainText()}
            return edited_date
        else:
            return None


    def editing_date(self, day_description: str, day_type: str, days_date: QDate):
        
        self.date_input.setDate(days_date)
        self.day_description_input.setText(day_description)
        self.day_type_input.setText(day_type)
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            edited_date = {'DAY_DESC': self.day_description_input.toPlainText(),
                           'DATE': self.date_input.date(),
                           'TYPE': self.day_type_input.toPlainText()}
            return edited_date
        else:
            return None
    

class MultipleDateEdit(QDialog):


    def __init__(self, parent = EventList):
        super(MultipleDateEdit, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("multiple_date_insertion.ui"), self)

        self.day_description_input = self.findChild(QTextEdit, "day_desc_textedit")
        self.day_type_input = self.findChild(QTextEdit, "day_type_textedit")
        self.from_date_input = self.findChild(QDateEdit, "dateEdit")
        self.till_date_input = self.findChild(QDateEdit, "dateEdit_2")
        self.dialog_options = self.findChild(QDialogButtonBox, "buttonBox")

        self.dialog_options.accepted.connect(self.accept) 
        self.dialog_options.rejected.connect(self.reject)


    def adding_new_date_range(self):
        self.from_date_input.setDateTime(QDateTime.currentDateTime())
        self.till_date_input.setDateTime(QDateTime.currentDateTime())
        edited_dates_list = []
        result = self.exec()
        
        if result == QDialog.DialogCode.Accepted:
            from_date = self.from_date_input.date()
            till_date = self.till_date_input.date()
            while  from_date <= till_date:
                edited_date = {'DAY_DESC': self.day_description_input.toPlainText(),
                                'DATE': from_date,
                                'TYPE': self.day_type_input.toPlainText()}
                edited_dates_list.append(edited_date)
                from_date = from_date.addDays(1)
            print(edited_dates_list)
            return edited_dates_list
        else:
            return None


# app = QApplication(sys.argv)
# window = DateEdit()
# window.show()
# sys.exit(app.exec())    


