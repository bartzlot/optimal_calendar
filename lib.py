#libraries
import typing

import pandas as pd

from PyQt6.QtWidgets import (QWidget, QApplication, 
                             QMainWindow, QCalendarWidget, 
                             QDateEdit, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem,
                             QDialog, QTextEdit, QDialogButtonBox)

from PyQt6.QtGui import (QPalette, QTextCharFormat, 
                         QColor, QPainter,)

from PyQt6.QtCore import (Qt, QDate, QDateTime, 
                          QRect, QPoint)
from PyQt6 import uic

import sys

#imports from different files
from database import DatabaseManager
from calendar_window import CalendarWindow
from event_list_window import EventList
