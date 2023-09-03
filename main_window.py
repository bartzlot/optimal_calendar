import typing
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QCalendarWidget, QDateEdit, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QTextCharFormat, QColor, QPainter
from PyQt6.QtCore import Qt, QDate, QDateTime, QRect, QPoint
from PyQt6 import uic
import sys
from database import DatabaseManager



class MainWindow(QMainWindow, DatabaseManager):


    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("window_design.ui", self)
        self.main_widget = self.findChild(QWidget, "centralwidget")
        self.cal = self.findChild(QCalendarWidget, "calendarWidget")
        self.start_date_box = self.findChild(QDateEdit, "startingDate")
        self.end_date_box = self.findChild(QDateEdit, "endingDate")
        self.lost_days = self.findChild(QLabel, "numberLostDays")
        self.date_select = self.findChild(QPushButton, "date_select_button")

        self.begin_date = None
        self.end_date = None

        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("lightblue"))
        self.highlight_format.setForeground(QColor("black"))
        self.cal.clicked.connect(self.date_is_clicked)
        self.date_select.clicked.connect(self.setting_date_using_boxes)

        self.holidays_format = QTextCharFormat()
        self.holidays_format.setBackground(QColor('orange'))
        self.holidays_format.setForeground(QColor('black'))

        self.holiday_highlighted_format = QTextCharFormat()
        self.holiday_highlighted_format.setBackground(QColor(255,213,128,255))
        self.holiday_highlighted_format.setForeground(QColor('black'))

        self.holidays_full = DatabaseManager.getting_data_excel(self, 'polish_database.xlsx')
        self.holidays_dates = DatabaseManager.extracting_dates(DatabaseManager(), self.holidays_full)
        
    def setting_current_date(self):
        self.start_date_box.setDateTime(QDateTime.currentDateTime())
        self.end_date_box.setDateTime(QDateTime.currentDateTime())


    def mark_holidays(self):
        for i in self.holidays_dates:
            print(i)
            self.cal.setDateTextFormat(i, self.holidays_format)


    def format_range(self, format):
        if self.begin_date and self.end_date:
            bd = min(self.begin_date, self.end_date)
            ed = max(self.begin_date, self.end_date)
            while bd <= ed:
                if bd in self.holidays_dates:
                    self.cal.setDateTextFormat(bd, self.holiday_highlighted_format)
                    bd = bd.addDays(1)
                else:
                    self.cal.setDateTextFormat(bd, format)
                    bd = bd.addDays(1)
        
    def setting_date_using_boxes(self):

        if self.start_date_box.date() > self.end_date_box.date() or self.end_date_box.date() < self.start_date_box.date():
            t = self.start_date_box.date()
            self.start_date_box.setDate(self.end_date_box.date())
            self.end_date_box.setDate(t)

        if self.end_date_box.date() < self.start_date_box.date():
            t = self.start_date_box.date()
            self.start_date_box.setDate(self.end_date_box.date())
            self.end_date_box.setDate(t)

        self.format_range(QTextCharFormat())
        self.begin_date = self.start_date_box.date()
        self.end_date = self.end_date_box.date()
        self.format_range(self.highlight_format)
        

    def date_is_clicked(self, date_val):
        # reset highlighting of previously selected date range
        self.mark_holidays()
        self.format_range(QTextCharFormat())
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier and self.begin_date:
            self.end_date = date_val
            self.end_date_box.setDate(date_val)
            self.format_range(self.highlight_format)
        else:
            self.begin_date = date_val
            self.start_date_box.setDate(date_val)
            self.end_date = None
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setting_current_date()
    window.mark_holidays()
    window.show()
    sys.exit(app.exec())