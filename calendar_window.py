from lib import *



class CalendarWindow(QMainWindow):


    def __init__(self, db_manager, parent = None):
        super(CalendarWindow, self).__init__(parent)
        uic.loadUi("window_design.ui", self)
        self.main_widget = self.findChild(QWidget, "centralwidget")
        self.cal = self.findChild(QCalendarWidget, "calendarWidget")
        self.start_date_box = self.findChild(QDateEdit, "startingDate")
        self.end_date_box = self.findChild(QDateEdit, "endingDate")
        self.lost_days_num = self.findChild(QLabel, "numberLostDays")
        self.date_select = self.findChild(QPushButton, "date_select_button")
        self.work_days_label = self.findChild(QLabel, "working_days_label")
        self.work_days_num = self.findChild(QLabel, "numberWorkDays")
        self.days_selected = self.findChild(QLabel, "days_selected_label")
        self.days_selected_num = self.findChild(QLabel, "DaysSelectedNumber")
        self.day_description = self.findChild(QLabel, "day_desc")
        self.db_manager = db_manager
        self.holidays_full = self.db_manager.getting_data_excel('polish_database.xlsx')
        self.holidays_dates = self.db_manager.extracting_dates(self.holidays_full)
        self.begin_date = None
        self.end_date = None

        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("lightblue"))
        self.highlight_format.setForeground(QColor("black"))

        self.holidays_format = QTextCharFormat()
        self.holidays_format.setBackground(QColor('orange'))
        self.holidays_format.setForeground(QColor('black'))

        self.holiday_highlighted_format = QTextCharFormat()
        self.holiday_highlighted_format.setBackground(QColor(255,213,128,255))
        self.holiday_highlighted_format.setForeground(QColor('black'))
        self.cal.clicked.connect(self.date_is_clicked)
        self.date_select.clicked.connect(self.setting_date_using_boxes)
        self.setting_current_date()
        self.mark_holidays()
        
    def setting_current_date(self):
        self.start_date_box.setDateTime(QDateTime.currentDateTime())
        self.end_date_box.setDateTime(QDateTime.currentDateTime())


    def mark_holidays_from_list(self, dates: list):

        for date in self.holidays_dates:
            self.cal.setDateTextFormat(date, QTextCharFormat())

        self.holidays_dates = dates

        for date in dates:
            self.cal.setDateTextFormat(date, self.holidays_format)


    def updating_database(self, database: list):
        self.holidays_full = database


    def mark_holidays(self):
        for i in self.holidays_dates:
            self.cal.setDateTextFormat(i, self.holidays_format)


    def update_calendar_by_list(self):
        self.mark_holidays()


    def format_range(self, format):
        if self.begin_date and self.end_date:
            bd = min(self.begin_date, self.end_date)
            ed = max(self.begin_date, self.end_date)
            w_days_count = self.counting_work_days(bd, ed)
            l_days_count = self.counting_lost_days(bd, ed)
            s_days_count = self.counting_selected_days(bd, ed)
            self.updating_counting_labels(l_days_count, w_days_count, s_days_count)
            while bd <= ed:
                if bd in self.holidays_dates:
                    self.cal.setDateTextFormat(bd, self.holiday_highlighted_format)
                    bd = bd.addDays(1)
                else:
                    self.cal.setDateTextFormat(bd, format)
                    bd = bd.addDays(1)
        

    def counting_work_days(self, start_selected: QDate, end_selected: QDate):
        WORKING_DAYS = [1, 2, 3, 4, 5]
        counter = 0
        while start_selected <= end_selected:
            if start_selected.dayOfWeek() in WORKING_DAYS and start_selected not in self.holidays_dates:
                counter += 1
            start_selected = start_selected.addDays(1) 
        return counter


    def counting_lost_days(self, start_selected: QDate, end_selected: QDate):
        counter = 0
        while start_selected <= end_selected:

            if start_selected in self.holidays_dates:
                counter += 1
            
            start_selected = start_selected.addDays(1)
        return counter


    def counting_selected_days(self, start_selected: QDate, end_selected: QDate):
        counter = 0
        while start_selected <= end_selected:
            counter += 1
            start_selected = start_selected.addDays(1) 
        return counter


    def updating_counting_labels(self, lost_days: int, work_days: int, selected_days: int):
        self.work_days_num.setText(str(work_days))
        self.lost_days_num.setText(str(lost_days))
        self.days_selected_num.setText(str(selected_days))


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
        self.updating_counting_labels(0, 0, 0)
        self.mark_holidays()
        self.format_range(QTextCharFormat())
        self.check_day_status(date_val)
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier and self.begin_date:
            self.end_date = date_val
            self.end_date_box.setDate(date_val)
            self.format_range(self.highlight_format)
        else:
            self.begin_date = date_val
            self.start_date_box.setDate(date_val)
            self.end_date = None


    def check_day_status(self, date: QDate):
        WORK_DAYS = [1, 2, 3, 4, 5]
        WEEK_DAYS_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_num = date.dayOfWeek()
        day_name = WEEK_DAYS_NAMES[day_num - 1]
        
        if date in self.holidays_dates:
            index = self.holidays_dates.index(date)
            self.day_description.setStyleSheet('color: orange')
            self.day_description.setText(f'Holiday: {day_name} \n{self.holidays_full[index]["DAY_DESC"]}')
        
        if date not in self.holidays_dates and day_num in WORK_DAYS:
            self.day_description.setStyleSheet('color: rgb(255, 203, 204)')
            self.day_description.setText(f'Work day: {day_name}')

        if date not in self.holidays_dates and day_num not in WORK_DAYS:
            self.day_description.setStyleSheet('color: rgb(255, 233, 204)')            
            self.day_description.setText(f'Weekend: {day_name}')



