from lib import *


class OptionsWindow(QMainWindow):

    calendar_update = pyqtSignal(list)
    holidays_changed = pyqtSignal(list)
    list_update = pyqtSignal(list)


    def __init__(self, db_manager, parent = None):
        super(OptionsWindow, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("settings.ui"), self)

        self.database_info_label = self.findChild(QLabel, "database_info_label")
        self.change_database_button = self.findChild(QPushButton, "change_database_button")
        self.marked_days_default_signature = self.findChild(QTextEdit, "marked_days_signature_edit")
        self.change_default_signature = self.findChild(QPushButton, "change_def_signature_button")
        self.defaults_button = self.findChild(QPushButton, "defaults_button")
        self.save_button = self.findChild(QPushButton, "save_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")

        self.db_manager = db_manager

        self.updating_default_signature()
        self.updating_database_info(self.db_manager.current_database)
        self.change_default_signature.clicked.connect(self.update_default_signature_button_event)
        self.change_database_button.clicked.connect(self.change_database_button_event)
        
        self.exit_button.clicked.connect(self.exit_button_event)


    def updating_default_signature(self):

        self.marked_days_default_signature.setText(self.db_manager.default_marked_signature)
        
    
    def update_default_signature_button_event(self):
        """Updating signature in database and other windows
        """
        env_file_path = DatabaseManager.creating_path_to_env_file()
        signature = self.marked_days_default_signature.toPlainText()

        if self.db_manager.default_marked_signature == signature:

            same_value_err = Errorhandler()
            same_value_err.error_handler("Default signature is the same, no need for changing...")
        
        if self.db_manager.default_marked_signature == signature:
            no_value_err = Errorhandler()
            no_value_err.error_handler("Default signature isn't set, so you have to set this along with currently loaded database")

        else:
            
            self.db_manager.database = DatabaseManager.getting_data_excel(DatabaseManager, self.db_manager.current_database)
            self.db_manager.updating_default_day_signature(signature)
            env_file_path = DatabaseManager.creating_path_to_env_file()
            set_key(env_file_path, "DEFAULT_HOLIDAY_SIGNATURE", signature)

            self.calendar_update.emit(self.db_manager.database)
            self.list_update.emit(self.db_manager.database)

            self.db_manager.saving_data_to_excel(self.db_manager.database, self.db_manager.current_database)

            self.db_manager.default_marked_signature = signature


    def updating_database_info(self, database_name: str):

        self.database_info_label.setText(database_name)


    def change_database_button_event(self): 
        """Changing database, from selected file in QFileDialog
        """
        starting_dir = pathlib.PurePath(__file__)
        starting_dir = starting_dir.parent.parent
        starting_dir = starting_dir.joinpath('databases')
        path = QFileDialog.getOpenFileName(self, 'Set Database File', str(starting_dir), "Excel files (*.xlsx)" )

        if path[0] != '':

            file_name = pathlib.Path(path[0]).name
            self.db_manager.current_database = file_name
            self.updating_database_info(file_name)
            self.getting_new_database_data(file_name)
            self.db_manager.default_marked_signature = ''
            self.updating_default_signature()
    

    def getting_new_database_data(self, file_name: str):
        """Gets new database from file if it's in correct template

        Args:
            file_name (str): filename
        """
        env_file_path = DatabaseManager.creating_path_to_env_file()

        try:
            
            self.db_manager.database = DatabaseManager.getting_data_excel(DatabaseManager, file_name)

            set_key(env_file_path, "DEFAULT_DATABASE", file_name)

            new_dates = self.db_manager.extracting_dates(self.db_manager.database)

            self.calendar_update.emit(self.db_manager.database)
            self.list_update.emit(self.db_manager.database)
            self.holidays_changed.emit(new_dates)

        except FileNotFoundError as fnf:

            file_err = Errorhandler()
            file_err.error_handler(fnf)
            file_err.exec()
            set_key(env_file_path, "DEFAULT_DATABASE", self.db_manager.LAST_DB)
            self.updating_database_info(self.db_manager.LAST_DB)

        except Exception:

            file_err = Errorhandler()
            file_err.error_handler("Wrong file data format or database empty...\n Switching to first opened database")
            file_err.exec()
            set_key(env_file_path, "DEFAULT_DATABASE", self.db_manager.LAST_DB)
            self.updating_database_info(self.db_manager.LAST_DB)


    def exit_button_event(self):
        self.close()
