import pandas as pd
from PyQt6.QtCore import Qt, QDate, QDateTime

class DatabaseManager():


    def __init__(self) -> None:
        self.df = None

    def getting_data_excel(self, directory: str):
        # polish_database.xlsx
        self.df = pd.read_excel(directory)
        self.df['DATE'] = self.df['DATE'].dt.strftime('%Y-%m-%d')

        
        for i, date in enumerate(self.df['DATE']):
            self.df['DATE'][i] = QDate.fromString(date, 'yyyy-MM-dd')
        
        self.data_dict = self.df.to_dict('records')
        return self.data_dict
    
    def extracting_dates(self, data_dict: dict):
        dates_data = []
        for i in data_dict:
            dates_data.append(i["DATE"])
        return dates_data

db = DatabaseManager()