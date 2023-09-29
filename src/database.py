from lib import *
class DatabaseManager():


    def __init__(self) -> None: 

        self.database = []
        self.dates_list = []
        self.current_database = ''

        load_dotenv()

        self.LAST_DB= os.getenv('DEFAULT_DATABASE')
        self.default_marked_signature = os.getenv('DEFAULT_HOLIDAY_SIGNATURE')


    def getting_data_excel(self, directory: str):
        """Gets data from excel file (in specified template)

        Args:
            directory (str): directory of database file

        Returns:
            list: database
        """
        df = pd.read_excel(DatabaseManager.creating_path_to_database_file(directory))

        df['DATE'] = df['DATE'].dt.strftime('%Y-%m-%d')

        for i, date in enumerate(df['DATE']):

            df['DATE'][i] = QDate.fromString(date, 'yyyy-MM-dd')

        self.current_database = directory
        data_dict = df.to_dict('records')

        return data_dict


    def extracting_dates(self, data_dict: dict):
        """Exstracts only dates from whole database

        Args:
            data_dict (dict): database

        Returns:
            list: only holidays dates extracted from database
        """
        dates_data = []

        for i in data_dict:
            dates_data.append(i["DATE"])

        return dates_data


    def saving_data_to_excel(self, database: list, file_name: str):
        """Saves database to excel file

        Args:
            database (list): database
            file_name (str): database file directory
        """
        for date in database:
            date['DATE'] = date['DATE'].toString('yyyy-MM-dd')

        df = pd.DataFrame.from_dict(database)
        
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')

        df.to_excel(DatabaseManager.creating_path_to_database_file(file_name), index=False)

        for date in database:

            date['DATE'] = QDate.fromString(date['DATE'], 'yyyy-MM-dd')


    def sorting_database(self, database: list, new_record: dict):
        """Sorts database after adding/changing values by dates

        Args:
            database (list): database
            new_record (dict): added/edited record

        Returns:
            list: sorted database
        """
        if len(database) == 1:

            if database[0]['DATE'] > new_record['DATE']:

                database.insert(0, new_record)

            else:
                database.append(new_record)
            
            return database

        if len(database) == 0:

            database.append(new_record)
            return database

        for index, record in enumerate(database):
            
            if record['DATE'] > new_record['DATE']:
                database.insert(index, new_record)
                return database
        database.append(new_record)
        return database


    def sorting_database_after_editing(self, database: list):

        def get_date(dictionary):
            return dictionary["DATE"]

        sorted_list = sorted(database, key=get_date)
        return sorted_list

    
    def editing_database(self, database: list, edited_record: dict, index: int):
        """Edititng specified index in database with given record

        Args:
            database (list): database
            edited_record (dict): edited record 
            index (int): index

        Returns:
            list: edited database
        """
        database[index] = edited_record
        # for i, record in enumerate(database):

        #     if record['DATE'] > edited_record['DATE']:
        #         database.insert(i, edited_record)
        #         database.pop(index)
        #         return database
        # database.pop(index)
        # database.append(edited_record)
        return database


    def deleting_records(self, database: list, index: set):
        """Deletes specified by index record from database

        Args:
            database (list): database
            index (set): index to delete

        Returns:
            list: updated database
        """
        for i, x in enumerate(index):

            del database[x-i]

        return database


    def creating_path_to_database_file(filename: str):

        file_path = pathlib.PurePath(__file__)
        file_path = file_path.parent.parent
        file_path = file_path.joinpath('databases', filename)

        return str(file_path)


    def creating_path_to_ui_file(filename: str):

        file_path = pathlib.PurePath(__file__)
        file_path = file_path.parent.parent
        file_path = file_path.joinpath('ui', filename)

        return str(file_path)


    def creating_path_to_env_file():

        file_path = pathlib.PurePath(__file__)
        file_path = file_path.parent
        file_path = file_path.joinpath('.env')

        return str(file_path)


    def updating_default_day_signature(self, new_signature: str):
        """Updates default holidays signature

        Args:
            new_signature (str): new signature
        """

        for date in self.database:

            if date['TYPE'] == self.default_marked_signature:

                date['TYPE'] = new_signature

        self.default_marked_signature = new_signature


class Errorhandler(QDialog):


    def __init__(self, parent = None):

        super(Errorhandler, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file('error_dialog.ui'), self)

        self.error_text_label = self.findChild(QLabel, "error_text_label")
        self.ok_button = self.findChild(QPushButton, "ok_button")

        self.ok_button.clicked.connect(self.ok_button_event)


    def error_handler(self, error_mess):
        """Error window with specified error message

        Args:
            error_mess (str, error): error message displayed in window
        """
        self.error_text_label.setText(str(error_mess))
        self.exec()
        self.show()


    def ok_button_event(self):
        self.close()
