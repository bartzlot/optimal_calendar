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
        self.database = db_manager.getting_data_excel(self.db_manager.LAST_DB)
        self.calendar_window_instance = calendar

        self.creating_table()
        self.inserting_data_to_list()

        self.add_button.clicked.connect(self.add_button_event)
        self.multiple_add_button.clicked.connect(self.multiple_add_button_event)
        self.edit_button.clicked.connect(self.edit_button_event)
        self.exit_button.clicked.connect(self.exit_button_event)
        self.del_button.clicked.connect(self.delete_button_event)


    def creating_table(self):
        """Creates list in window
        """
        self.holidays_list.insertColumn(0)
        self.holidays_list.insertColumn(1)
        self.holidays_list.insertColumn(2)
        self.holidays_list.setHorizontalHeaderLabels(('Day description', 'Date', 'Day type'))
        self.holidays_list.setColumnWidth(0, 350)
        self.holidays_list.setColumnWidth(1, 105)
        self.holidays_list.setColumnWidth(2, 105)


    def inserting_data_to_list(self):
        """Inserts database into list
        """
        for index, records in enumerate(self.database):

            temp_date_in_str = records['DATE'].toString("dd.MM.yyyy")
            self.holidays_list.insertRow(index)
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(temp_date_in_str))
            self.holidays_list.setItem(index, 2, QTableWidgetItem(records['TYPE']))


    def updating_list_by_changing_db(self, new_db: list):
        """Update list if database was changed

        Args:
            new_db (list): new database
        """
        self.database = new_db
        self.updating_list()


    def clear_list(self):

        self.holidays_list.clear()


    def updating_list(self):
        """Updates list after adding new date, editing, deleting
        """
        self.holidays_list.setRowCount(0)
        for index, records in enumerate(self.database):
            self.holidays_list.insertRow(index)
            temp_date_in_str = records['DATE'].toString("dd.MM.yyyy")
            self.holidays_list.setItem(index, 0, QTableWidgetItem(records['DAY_DESC']))
            self.holidays_list.setItem(index, 1, QTableWidgetItem(temp_date_in_str))
            self.holidays_list.setItem(index, 2, QTableWidgetItem(records['TYPE']))


    def add_button_event(self):
        """Button event
        """
        add_action = DateEdit(self)
        new_date = add_action.adding_new_date()

        if new_date is not None:
            print(self.database)
            self.database = self.db_manager.sorting_database(self.database, new_date)

            self.dates_list = self.db_manager.extracting_dates(self.database)
            self.updating_list()
            self.data_added.emit(self.dates_list)
            self.database_updated.emit(self.database)
            DatabaseManager.saving_data_to_excel(DatabaseManager, self.database, self.db_manager.current_database)

        else: pass
    

    def multiple_add_button_event(self):
        """Button event
        """
        add_multiple_action = MultipleDateEdit(self)
        new_dates_list = add_multiple_action.adding_new_date_range()

        if new_dates_list is not None:

            for date in new_dates_list:

                self.database = self.db_manager.sorting_database(self.database, date)

            self.dates_list = self.db_manager.extracting_dates(self.database)       
            self.updating_list()
            self.data_added.emit(self.dates_list)
            self.database_updated.emit(self.database)
            DatabaseManager.saving_data_to_excel(DatabaseManager, self.database, self.db_manager.current_database)

        else: pass
        

    def edit_button_event(self):
        """Button event
        """
        edit_action = DateEdit(self)
        new_date = []
        selected_rows = set()
        selected_items = self.holidays_list.selectedItems()

        if len(selected_items) == 0:

            empty_err = Errorhandler()
            empty_err.error_handler("You have to select some rows to continue editing...")

        for item in selected_items:

            selected_rows.add(item.row())

        for data in selected_rows:

            new_date = edit_action.editing_date(self.database[data]['DAY_DESC'], self.database[data]['TYPE'], self.database[data]['DATE'])

            if new_date is not None:

                self.database = self.db_manager.editing_database(self.database, new_date, data)
    
            else: continue

        self.database = self.db_manager.sorting_database_after_editing(self.database)
        self.updating_list()
        self.dates_list = self.db_manager.extracting_dates(self.database)
        self.data_updated.emit(self.dates_list)
        self.database_updated.emit(self.database)
        DatabaseManager.saving_data_to_excel(DatabaseManager, self.database, self.db_manager.current_database)


    def delete_button_event(self):
        """Button event
        """
        selected_rows = set()
        selected_items = self.holidays_list.selectedItems()

        if len(selected_items) == 0:

            empty_err = Errorhandler()
            empty_err.error_handler("You have to select some rows to continue editing...")

        else:

            deleting_confirmation = DeletingConfirm(self)
            deleting_status = deleting_confirmation.getting_deleting_status()

            if deleting_status is True:

                for item in selected_items:

                    selected_rows.add(item.row())

                if len(self.database) == len(selected_items):
                    last_record = Errorhandler()
                    last_record.error_handler("You cannot delete whole database, change file...")
                else:
                    self.database = self.db_manager.deleting_records(self.database, selected_rows)
                    self.updating_list()
                    self.dates_list = self.db_manager.extracting_dates(self.database)
                    self.data_updated.emit(self.dates_list)
                    self.database_updated.emit(self.database)
                    DatabaseManager.saving_data_to_excel(DatabaseManager, self.database, 'polish_database.xlsx')

            else: pass


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
        """Adding new date action

        Returns:
            dict, None: depends on input if accepted returns dict of day
        """
        self.date_input.setDateTime(QDateTime.currentDateTime())
        result = self.exec()

        if result == QDialog.DialogCode.Accepted:

            edited_date = {'DAY_DESC': self.day_description_input.toPlainText(),
                           'DATE': self.date_input.date(),
                           'TYPE': self.day_type_input.toPlainText()}
            print(edited_date)
            return edited_date
        
        else:

            return None


    def editing_date(self, day_description: str, day_type: str, days_date: QDate):
        """Edits existing record in database

        Args:
            day_description (str): day desc
            day_type (str): day type (holiday etc...)
            days_date (QDate): date

        Returns:
            dict, None: depends on input if accepted returns dict of edited day data
        """
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
        """Adding date range (vacation etc...), multi days input

        Returns:
            dict, None: depends on input if accepted returns dict of day
        """
        self.from_date_input.setDateTime(QDateTime.currentDateTime())
        self.till_date_input.setDateTime(QDateTime.currentDateTime())
        edited_dates_list = []
        result = self.exec()
        
        if result == QDialog.DialogCode.Accepted:

            from_date = self.from_date_input.date()
            till_date = self.till_date_input.date()
            
            if from_date > till_date:

                from_date, till_date = till_date, from_date

            while  from_date <= till_date:

                edited_date = {'DAY_DESC': self.day_description_input.toPlainText(),
                                'DATE': from_date,
                                'TYPE': self.day_type_input.toPlainText()}
                edited_dates_list.append(edited_date)
                from_date = from_date.addDays(1)

            return edited_dates_list
        
        else:

            return None


class DeletingConfirm(QDialog):


    def __init__(self, parent = EventList):
        super(DeletingConfirm, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("delete_confirmation.ui"), self)

        self.dialog_options = self.findChild(QDialogButtonBox, "dialog_yes_no")
    
        self.dialog_options.accepted.connect(self.accept)
        self.dialog_options.rejected.connect(self.reject)


    def getting_deleting_status(self):
        """Deleting confirmation window

        Returns:
            bool: deletion status
        """
        result = self.exec()

        if result == QDialog.DialogCode.Accepted:

            return True
        
        else:

            return False
