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
        self.change_database_button.clicked.connect(self.change_database_button_event)
        
        self.exit_button.clicked.connect(self.exit_button_event)


    def updating_default_signature(self):
        self.marked_days_default_signature.setText(self.db_manager.default_marked_signature)

    
    def updating_database_info(self, database_name: str):
        self.database_info_label.setText(database_name)


    def change_database_button_event(self): 
        starting_dir = pathlib.PurePath(__file__)
        starting_dir = starting_dir.parent.parent
        starting_dir = starting_dir.joinpath('databases')
        path = QFileDialog.getOpenFileName(self, 'Set Database File', str(starting_dir), "Excel files (*.xlsx)" )

        if path[0] != '':
            file_name = pathlib.Path(path[0]).name
            self.db_manager.current_database = file_name
            self.updating_database_info(file_name)

            self.getting_new_database_data(file_name)
    

    def getting_new_database_data(self, file_name: str):
        self.db_manager.database = DatabaseManager.getting_data_excel(DatabaseManager, file_name)
        env_file_path = DatabaseManager.creating_path_to_env_file()
        set_key(env_file_path, "DEFAULT_DATABASE", file_name)
        new_dates = self.db_manager.extracting_dates(self.db_manager.database)

        self.calendar_update.emit(self.db_manager.database)
        self.list_update.emit(self.db_manager.database)
        self.holidays_changed.emit(new_dates)


    def defaults_button_event(self):#TODO
        pass


    def save_button_event(self):#TODO
        pass


    def exit_button_event(self):
        self.close()

