from lib import *


class CalendarWindow(QMainWindow):


    def __init__(self, db_manager, parent = None):

        super(CalendarWindow, self).__init__(parent)

        uic.loadUi(DatabaseManager.creating_path_to_ui_file("calendar.ui"), self)

        self.main_widget = self.findChild(QWidget, "centralwidget")
        self.cal = self.findChild(QCalendarWidget, "calendarWidget")
        self.start_date_box = self.findChild(QDateEdit, "startingDate")
        self.end_date_box = self.findChild(QDateEdit, "endingDate")
        self.lost_days_num = self.findChild(QLabel, "numberLostDays")
        self.date_select = self.findChild(QPushButton, "date_select_button")
        self.calculate_work_button = self.findChild(QPushButton, "calculate_workflow_button")
        self.optimize_work_button = self.findChild(QPushButton, "optimize_workflow_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")        
        self.work_days_label = self.findChild(QLabel, "working_days_label")
        self.work_days_num = self.findChild(QLabel, "numberWorkDays")
        self.days_selected = self.findChild(QLabel, "days_selected_label")
        self.days_selected_num = self.findChild(QLabel, "DaysSelectedNumber")
        self.day_description = self.findChild(QLabel, "day_desc")

        self.db_manager = db_manager
        self.holidays_full = self.db_manager.getting_data_excel(self.db_manager.LAST_DB)
        self.holidays_dates = self.db_manager.extracting_dates(self.holidays_full)
            
        self.begin_date = None
        self.end_date = None

        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("lightblue"))
        self.highlight_format.setForeground(QColor("black"))

        self.holidays_format = QTextCharFormat()
        self.holidays_format.setBackground(QColor(255, 128, 128))
        self.holidays_format.setForeground(QColor('black'))

        self.holiday_highlighted_format = QTextCharFormat()
        self.holiday_highlighted_format.setBackground(QColor(255,213,128,255))
        self.holiday_highlighted_format.setForeground(QColor('black'))

        self.cal.clicked.connect(self.date_is_clicked)
        self.exit_button.clicked.connect(self.exit_button_event)
        self.date_select.clicked.connect(self.setting_date_using_boxes)
        self.calculate_work_button.clicked.connect(self.calculate_workflow_button_event)
        self.optimize_work_button.clicked.connect(self.optimize_workflow_button_event)

        self.setting_current_date()
        self.mark_holidays()


    def setting_current_date(self):
        """Setting current date in calendar"""

        self.start_date_box.setDateTime(QDateTime.currentDateTime())
        self.end_date_box.setDateTime(QDateTime.currentDateTime())


    def mark_holidays_from_list(self, dates: list):
        """Marks holidays from database (given list)

        Args:
            dates (list): list containing only dates of holidays
        """

        for date in self.holidays_dates:
            self.cal.setDateTextFormat(date, QTextCharFormat())

        self.holidays_dates = dates

        for date in dates:
            self.cal.setDateTextFormat(date, self.holidays_format)


    def updating_database(self, database: list):
        """Updates database using database from the other window wchich was changed

        Args:
            database (list): new edited database
        """
        self.holidays_full = database


    def mark_holidays(self):
        """Marking holidays (changing color in calendar)
        """
        for i in self.holidays_dates:
            self.cal.setDateTextFormat(i, self.holidays_format)


    def format_range(self, format: QTextCharFormat):
        """Formating date range selected by user (changing color)

        Args:
            format (QTextCharFormat): date box format (color etc...)
        """
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
        """Counts working days within selected date range

        Args:
            start_selected (QDate): starting date selected
            end_selected (QDate): ending date selected

        Returns:
            int: amount of work days
        """
        WORKING_DAYS = [1, 2, 3, 4, 5]
        counter = 0

        while start_selected <= end_selected:

            if start_selected.dayOfWeek() in WORKING_DAYS and start_selected not in self.holidays_dates:
                counter += 1

            start_selected = start_selected.addDays(1) 

        return counter


    def counting_lost_days(self, start_selected: QDate, end_selected: QDate):
        """Counts lost days within selected date range

        Args:
            start_selected (QDate): starting date selected
            end_selected (QDate): ending date selected

        Returns:
            int: amount of lost days
        """
        counter = 0

        while start_selected <= end_selected:

            if start_selected in self.holidays_dates:
                counter += 1
            
            start_selected = start_selected.addDays(1)

        return counter


    def counting_selected_days(self, start_selected: QDate, end_selected: QDate):
        """Counts selected days within selected date range

        Args:
            start_selected (QDate): starting date selected
            end_selected (QDate): ending date selected

        Returns:
            int: amount of selected days
        """
        counter = 0

        while start_selected <= end_selected:

            counter += 1
            start_selected = start_selected.addDays(1) 

        return counter


    def updating_counting_labels(self, lost_days: int, work_days: int, selected_days: int):
        """Updates labels assigned to counted days in selected range

        Args:
            lost_days (int): lost days amount
            work_days (int): work days amount
            selected_days (int): selected days amount
        """
        self.work_days_num.setText(str(work_days))
        self.lost_days_num.setText(str(lost_days))
        self.days_selected_num.setText(str(selected_days))


    def setting_date_using_boxes(self):
        """Setting date range using QDateEdit boxes
        """

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
        """Defines which date is clicked on calendar and update description, counting label, changes it in date boxes...

        Args:
            date_val (QDate): _description_
        """
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
        """Checks day status after clicking it and sets description depending on week day/holiday...

        Args:
            date (QDate): date clicked
        """
        WORK_DAYS = [1, 2, 3, 4, 5]
        WEEK_DAYS_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_num = date.dayOfWeek()
        day_name = WEEK_DAYS_NAMES[day_num - 1]
        
        if date in self.holidays_dates:
            index = self.holidays_dates.index(date)
            self.day_description.setStyleSheet('color: rgb(255, 128, 128); font-size: 30px;')
            self.day_description.setText(f'{self.holidays_full[index]["TYPE"]}: {day_name} \n{self.holidays_full[index]["DAY_DESC"]}')
        
        if date not in self.holidays_dates and day_num in WORK_DAYS:
            self.day_description.setStyleSheet('color: #5C7D8A; font-size: 30px;')
            self.day_description.setText(f'Work day: {day_name}')

        if date not in self.holidays_dates and day_num not in WORK_DAYS:
            self.day_description.setStyleSheet('color: rgb(255, 233, 204); font-size: 30px;')  
            self.day_description.setText(f'Weekend: {day_name}')


    def calculate_workflow_button_event(self):
        """Button click event
        """
        if self.begin_date == None or self.end_date == None:

            date_select_error = Errorhandler()
            date_select_error.error_handler("Please select date range...")

        else:

            calculate_workflow = MeetingCalculator(self, self.begin_date, self.end_date, self.holidays_dates)
            calculate_workflow.show()
    

    def optimize_workflow_button_event(self):
        """button event
        """
        if self.begin_date == None or self.end_date == None:

            date_select_error = Errorhandler()
            date_select_error.error_handler("Please select date range...")

        else:

            optimize_workflow = MeetingOptimizer(self, self.begin_date, self.end_date, self.holidays_dates)
            optimize_workflow.show()


    def exit_button_event(self):
        
        self.close()

    






