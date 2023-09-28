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
        
        df = pd.read_excel(DatabaseManager.creating_path_to_database_file(directory))

        df['DATE'] = df['DATE'].dt.strftime('%Y-%m-%d')

        for i, date in enumerate(df['DATE']):
            df['DATE'][i] = QDate.fromString(date, 'yyyy-MM-dd')
        self.current_database = directory
        data_dict = df.to_dict('records')

        return data_dict


    def extracting_dates(self, data_dict: dict):
        dates_data = []
        for i in data_dict:
            dates_data.append(i["DATE"])
        return dates_data


    def saving_data_to_excel(self, database: list, file_name: str):

        for date in database:
            date['DATE'] = date['DATE'].toString('yyyy-MM-dd')

        df = pd.DataFrame.from_dict(database)
        
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')

        df.to_excel(DatabaseManager.creating_path_to_database_file(file_name), index=False)

        for date in database:
            date['DATE'] = QDate.fromString(date['DATE'], 'yyyy-MM-dd')


    def sorting_database(self, database: list, new_record: dict):

        for index, record in enumerate(database):
            if record['DATE'] > new_record['DATE']:
                database.insert(index, new_record)
                break
        return database

    
    def editing_database(self, database: list, edited_record: dict, index: int):
        database[index] = edited_record
        return database


    def deleting_records(self, database: list, index: set):
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
        self.error_text_label.setText(str(error_mess))
        self.exec()
        self.show()

    def ok_button_event(self):
        self.close()

