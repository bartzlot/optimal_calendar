from lib import *

class MeetingCalculator(QMainWindow):


    def __init__(self, parent, bd, ed, dt):
        super(MeetingCalculator, self).__init__(parent)
        uic.loadUi(DatabaseManager.creating_path_to_ui_file("calculating_meeting_loses.ui"), self)

        self.monday_check = self.findChild(QCheckBox, "monday_check")
        self.tuesday_check = self.findChild(QCheckBox, "tuesday_check")
        self.wendesday_check = self.findChild(QCheckBox, "wednesday_check")
        self.thursday_check = self.findChild(QCheckBox, "thursday_check")
        self.friday_check = self.findChild(QCheckBox, "friday_check")
        self.saturday_check = self.findChild(QCheckBox, "saturday_check")
        self.sunday_check = self.findChild(QCheckBox, "sunday_check")

        self.interval_specifier = self.findChild(QComboBox, "interval_checkbox")

        

        self.calculate_button = self.findChild(QPushButton, "calculate_button")
        self.days_lost = self.findChild(QLabel, "days_lost")
        self.working_days = self.findChild(QLabel, "working_days")
        self.selected_days = self.findChild(QLabel, "selected_days")

        self.beg_date = bd
        self.end_date = ed
        self.database_copy = dt


        self.calculate_button.clicked.connect(self.calculating_workflow)


    def getting_checks_state(self):
        days_selected = []

        if self.monday_check.isChecked():
            days_selected.append(1)

        if self.tuesday_check.isChecked():
            days_selected.append(2)

        if self.wendesday_check.isChecked():
            days_selected.append(3)

        if self.thursday_check.isChecked():
            days_selected.append(4)

        if self.friday_check.isChecked():
            days_selected.append(5)

        if self.saturday_check.isChecked():
            days_selected.append(6)

        if self.sunday_check.isChecked():
            days_selected.append(7)

        return days_selected
    

    def getting_interval_state(self):
        interval_selected = self.interval_specifier.currentIndex()

        return interval_selected
    

    def calculating_workflow(self):

        WORKING_DAYS = self.getting_checks_state()
        days_lost = 0
        days_work = 0
        days_selected = 0 

        starting_date = self.beg_date

        while starting_date <= self.end_date:

            if starting_date in self.database_copy and starting_date.dayOfWeek() in WORKING_DAYS:
                days_lost += 1

            if starting_date.dayOfWeek() in WORKING_DAYS and starting_date not in self.database_copy:
                days_work += 1

            days_selected += 1
            starting_date = starting_date.addDays(1)

        self.days_lost.setText(str(days_lost))
        self.working_days.setText(str(days_work))
        self.selected_days.setText(str(days_selected))


