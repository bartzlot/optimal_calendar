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
        self.exit_button = self.findChild(QPushButton, "exit_button")

        self.days_lost = self.findChild(QLabel, "days_lost")
        self.working_days = self.findChild(QLabel, "working_days")
        self.selected_days = self.findChild(QLabel, "selected_days")
        self.date_from = self.findChild(QLabel, "date_from")
        self.date_till = self.findChild(QLabel, "date_till")

        self.beg_date = bd
        self.end_date = ed
        self.database_copy = dt


        self.date_from.setText(bd.toString("dd-MM-yyyy"))
        self.date_till.setText(ed.toString("dd-MM-yyyy"))
        self.calculate_button.clicked.connect(self.calculating_workflow)
        self.exit_button.clicked.connect(self.exit_button_event)


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
        INTERVAL_SETTING = self.getting_interval_state()

        if INTERVAL_SETTING == 0:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 1)

        if INTERVAL_SETTING == 1:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 2)

        if INTERVAL_SETTING == 2:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 3)

        if INTERVAL_SETTING == 3:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 4)

        if INTERVAL_SETTING == 4:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 8)

        if INTERVAL_SETTING == 5:

            days_lost, days_work, days_selected = self.calculate_others(self.beg_date, self.end_date, WORKING_DAYS, 12)

        self.days_lost.setText(str(days_lost))
        self.working_days.setText(str(days_work))
        self.selected_days.setText(str(days_selected))


    def calculate_others(self, starting_date: QDate, ending_date: QDate, work_days: list, interval: int):

        days_lost = 0
        days_work = 0
        days_selected = 0
        weeks_count = 0
        current_week = starting_date.weekNumber()

        while starting_date <= self.end_date:

            if starting_date.weekNumber() != current_week:

                current_week = starting_date.weekNumber()
                weeks_count += 1 

            if weeks_count % interval == 0:

                if starting_date in self.database_copy and starting_date.dayOfWeek() in work_days:
                    days_lost += 1

                if starting_date.dayOfWeek() in work_days and starting_date not in self.database_copy:
                    days_work += 1

            days_selected += 1
            starting_date = starting_date.addDays(1)
        
        return days_lost, days_work, days_selected
    

    def exit_button_event(self):
        self.close()


class MeetingOptimizer(QMainWindow):


    def __init__(self, parent, bd, ed, dt):
        super(MeetingOptimizer, self).__init__(parent)

        uic.loadUi(DatabaseManager.creating_path_to_ui_file("optimizing_meetings.ui"), self)

        self.monday_check = self.findChild(QCheckBox, "monday_check")
        self.tuesday_check = self.findChild(QCheckBox, "tuesday_check")
        self.wendesday_check = self.findChild(QCheckBox, "wednesday_check")
        self.thursday_check = self.findChild(QCheckBox, "thursday_check")
        self.friday_check = self.findChild(QCheckBox, "friday_check")
        self.saturday_check = self.findChild(QCheckBox, "saturday_check")
        self.sunday_check = self.findChild(QCheckBox, "sunday_check")
        self.unoptimize_check = self. findChild(QCheckBox, "unoptimize_check")

        self.interval_specifier = self.findChild(QComboBox, "interval_checkbox")

        self.most_optimized_days = self.findChild(QLabel, "optimized_days_label")
        self.date_from = self.findChild(QLabel, "date_from")
        self.date_till = self.findChild(QLabel, "date_till")

        self.optimize_button = self.findChild(QPushButton, "optimize_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")

        self.beg_date = bd
        self.end_date = ed
        self.database_copy = dt

        self.date_from.setText(bd.toString("dd-MM-yyyy"))
        self.date_till.setText(ed.toString("dd-MM-yyyy"))
        self.optimize_button.clicked.connect(self.optimize_workflow_button_event)
        self.exit_button.clicked.connect(self.exit_button_event)


    def getting_checks_state(self):
        days_selected = []

        if self.monday_check.isChecked():
            days_selected.append(0)

        if self.tuesday_check.isChecked():
            days_selected.append(1)

        if self.wendesday_check.isChecked():
            days_selected.append(2)

        if self.thursday_check.isChecked():
            days_selected.append(3)

        if self.friday_check.isChecked():
            days_selected.append(4)

        if self.saturday_check.isChecked():
            days_selected.append(5)

        if self.sunday_check.isChecked():
            days_selected.append(6)

        return days_selected
    

    def getting_interval_state(self):
        interval_selected = self.interval_specifier.currentIndex()

        return interval_selected


    def creating_days_data(self):

        WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_data = []
        EXCLUDED_DAYS = self.getting_checks_state()

        for num, data in enumerate(WEEK_DAYS):

            if num in EXCLUDED_DAYS:

                exclusion_state = True

            else:

                exclusion_state = False

            day_dataset = {'name' : data,
                           'days_lost': 0,
                           'is_excluded': exclusion_state}
            days_data.append(day_dataset)
        
        return days_data


    def optimize_workflow_button_event(self):

        INTERVAL_SETTING = self.getting_interval_state()

        most_efficient_days = []

        

        if INTERVAL_SETTING == 0:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 1)

        if INTERVAL_SETTING == 1:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 2)

        if INTERVAL_SETTING == 2:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 3)

        if INTERVAL_SETTING == 3:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 4)

        if INTERVAL_SETTING == 4:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 8)

        if INTERVAL_SETTING == 5:

            most_efficient_days = self.optimize_workflow_logic(self.beg_date, self.end_date, 12)

        most_optimal_label = ''

        for day in most_efficient_days:

            most_optimal_label += day['name'] + '\n'
        
        most_optimal_label += 'Days Lost:' + str(most_efficient_days[0]['days_lost'])

        self.most_optimized_days.setText(most_optimal_label)


    def optimize_workflow_logic(self, starting_date: QDate, ending_date: QDate, interval: int):

        days_data = self.creating_days_data()

        starting_week_num = starting_date.weekNumber()

        first_holiday_index = self.finding_nearest_holiday_index(starting_date)

        last_holiday_index = self.finding_last_holiday_index(ending_date, first_holiday_index) + 1

        for i in range(first_holiday_index, last_holiday_index, 1):
            
            if (self.database_copy[i].weekNumber()[0] - starting_week_num[0]) % interval == 0:

                date_day_of_week_number = self.database_copy[i].dayOfWeek() - 1

                if days_data[date_day_of_week_number]['is_excluded'] is False:

                    days_data[date_day_of_week_number]['days_lost'] += 1

                else:
                    pass
        
        if self.unoptimize_check.isChecked():

            most_optimal_days = self.finding_unoptimized_days(days_data)

        else:
            most_optimal_days = self.finding_most_optimal_days(days_data)

        return most_optimal_days


    def finding_most_optimal_days(self, days_data: list):
        most_optimal_days = []
        included_days_only = []

        for day in days_data:

            if day['is_excluded'] is False:

                included_days_only.append(day)

        min_days_lost = min(included_days_only, key=lambda x:x['days_lost'])

        for day in included_days_only:
            if day['days_lost'] == min_days_lost['days_lost']:

                most_optimal_days.append(day)
            
        return most_optimal_days


    def finding_unoptimized_days(self, days_data: list):
        unoptimized_days = []
        included_days_only = []

        for day in days_data:

            if day['is_excluded'] is False:

                included_days_only.append(day)

        min_days_lost = max(included_days_only, key=lambda x:x['days_lost'])

        for day in included_days_only:
            if day['days_lost'] == min_days_lost['days_lost']:

                unoptimized_days.append(day)
            
        return unoptimized_days

    def finding_nearest_holiday_index(self, starting_date:QDate):

        nearest_holiday_index = 0

        for ind, date in enumerate(self.database_copy):
            
            if date >= starting_date:

                nearest_holiday_index = ind

                return nearest_holiday_index
    

    def finding_last_holiday_index(self, ending_date: QDate, start_index: int): 

        last_holiday_index = 0

        for i in range(start_index, len(self.database_copy)):
            
            if self.database_copy[i] > ending_date:

                last_holiday_index = i - 1

                return last_holiday_index
            
            if self.database_copy[i] == ending_date:

                last_holiday_index = i

                return last_holiday_index
                

    def exit_button_event(self):
        self.close()

        

