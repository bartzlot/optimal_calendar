#libraries
import pathlib

import pandas as pd
pd.options.mode.chained_assignment = None

import copy

from dotenv import set_key, load_dotenv

from PyQt6.QtWidgets import (QWidget, QApplication, 
                             QMainWindow, QCalendarWidget, 
                             QDateEdit, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem,
                             QDialog, QTextEdit, QDialogButtonBox,
                             QFileDialog, QCheckBox, QComboBox)

from PyQt6.QtGui import (QPalette, QTextCharFormat, 
                         QColor, QPainter, QCloseEvent)

from PyQt6.QtCore import (Qt, QDate, QDateTime, 
                          QRect, QPoint, pyqtSignal)
from PyQt6 import uic

import sys

import os

#imports from different files
from database import DatabaseManager, Errorhandler
from options_window import OptionsWindow
from meeting_optimizer import MeetingCalculator, MeetingOptimizer
from calendar_window import CalendarWindow
from event_list_window import EventList
from main_menu import MainMenu


