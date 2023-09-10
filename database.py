from lib import *

class DatabaseManager():

    def getting_data_excel(self, directory: str):
        # polish_database.xlsx
        df = pd.read_excel(directory)
        df['DATE'] = df['DATE'].dt.strftime('%Y-%m-%d')

        for i, date in enumerate(df['DATE']):
            df['DATE'][i] = QDate.fromString(date, 'yyyy-MM-dd')
        
        data_dict = df.to_dict('records')
        return data_dict
    
    def extracting_dates(self, data_dict: dict):
        dates_data = []
        for i in data_dict:
            dates_data.append(i["DATE"])
        return dates_data
    
    def saving_data_to_excel(self, database: list, file_name: str):
        for i, date in enumerate(database):
            database[i]['DATE'] = date['DATE'].toString('yyyy/MM/dd')
        df = pd.DataFrame.from_dict(database)
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y/%m/%d')
        df.to_excel(file_name)


    def sorting_database(self, database: list, new_record: dict):

        for index, record in enumerate(database):
            if record['DATE'] > new_record['DATE']:
                database.insert(index, new_record)
                break
        return database

    
    def editing_database(self, database: list, edited_record: dict, index: int):
        database[index] = edited_record
        return database


    def deleting_records(self, database: list, index: int):
        del database[index]
        return database
db = DatabaseManager()

