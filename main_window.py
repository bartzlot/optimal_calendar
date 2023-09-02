import typing
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QCalendarWidget, QDateEdit, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6 import uic
import sys



class MainWindow(QMainWindow):
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


        
    def setting_current_date(self):
        self.start_date_box.setDateTime(QDateTime.currentDateTime())
        self.end_date_box.setDateTime(QDateTime.currentDateTime())


        

    def format_range(self, format):
        if self.begin_date and self.end_date:
            bd = min(self.begin_date, self.end_date)
            ed = max(self.begin_date, self.end_date)
            while bd <= ed:
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
    window.show()
    sys.exit(app.exec())