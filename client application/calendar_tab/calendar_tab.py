from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QGraphicsDropShadowEffect, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QDate
from datetime import date, timedelta

from qfluentwidgets import CalendarPicker, setTheme, Theme


class CalendarTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 30)
        self.grid = QGridLayout(self)
        self.calendarWindow = QMainWindow()
        self.calendarWindow.setProperty("tasksTopMenu", True)
        self.calendarWidget = QWidget()
        self.calendarWindow.setCentralWidget(self.calendarWidget)
        self.calendarGrid = QGridLayout(self.calendarWidget)
        self.calendarGrid.setContentsMargins(0, 0, 20, 0)

        self.calendarController = QWidget()
        self.calendarController.setFixedHeight(70)
        self.calendarControllerGrid = QGridLayout(self.calendarController)
        self.picker = CalendarPicker(self)
        self.picker.dateChanged.connect(self.datePicked)
        self.picker.setFixedWidth(140)
        self.monthLabel = QLabel("Month - YYYY")
        self.monthLabel.setStyleSheet("font-weight:bold;font-family:arial")
        self.calendarControllerGrid.addWidget(self.monthLabel, 0, 0)
        self.calendarControllerGrid.addWidget(self.picker, 0, 1)

        self.calendarView = QTableWidget(24, 7)
        self.parent = mainwindow
        self.calendarView.setHorizontalHeaderLabels(["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"])
        self.calendarView.setVerticalHeaderLabels(["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM","3 PM","4 PM","5 PM","6 PM","7 PM","8 PM","9 PM","10 PM","11 PM"])
        self.calendarView.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.selectedColumn = None
        font = QFont()
        font.setFamily("verdana")
        font.setPointSize(10)
        self.calendarView.horizontalHeader().setFont(font)
        self.calendarView.setFont(font)
        self.calendarView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.calendarView.setSelectionMode(QAbstractItemView.NoSelection)
        self.calendarView.setShowGrid(False)
        self.calendarView.horizontalHeader().sectionDoubleClicked.connect(self.focusColumn)
        self.calendarView.horizontalHeader().setStyleSheet("::section{border-right:none;padding-left:5px;padding-right:5px;}")
        self.calendarView.verticalHeader().setStyleSheet("::section{border:none;border-right:1px solid rgba(80,80,80,60);background:transparent;padding-bottom:22px;}")
        self.calendarView.horizontalHeader().setMinimumSectionSize(70)
        self.calendarView.verticalHeader().setMinimumSectionSize(35)
        self.calendarView.horizontalHeader().setSectionsClickable(False)
        self.calendarView.setProperty("calendarTable", True)
        for col in range(0, self.calendarView.columnCount()):
            self.calendarView.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        for row in range(0, self.calendarView.rowCount()):
            self.calendarView.verticalHeader().setSectionResizeMode(row, QHeaderView.Stretch)

        self.calendarGrid.addWidget(self.calendarController, 0, 0)
        self.calendarGrid.addWidget(self.calendarView, 1, 0)
        self.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.calendarWindow)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))


        self.picker.setDate(QDate(date.today().year,date.today().month,date.today().day))

        self.calendarWindow.setGraphicsEffect(boxShadow)

    def focusColumn(self, column):
        if self.selectedColumn == column:
            self.calendarView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
            self.selectedColumn = None
            for col in range(0, self.calendarView.columnCount()):
                self.calendarView.horizontalHeader().showSection(col)
        else:
            self.selectedColumn = column
            self.calendarView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            for col in range(0, self.calendarView.columnCount()):
                if column != col:
                    self.calendarView.horizontalHeader().hideSection(col)
                else:
                    self.calendarView.horizontalHeader().showSection(col)

    def datePicked(self, date):
        days_of_week = []
        years_months = {}
        sunday = date.toPyDate() - timedelta(days=int(date.toPyDate().strftime("%w")))
        for i in range(7):
            current_date = sunday + timedelta(days=i)
            day_of_week = current_date.day
            days_of_week.append(day_of_week)
            if current_date.year not in years_months.keys():
                years_months[current_date.year] = []
                years_months[current_date.year].append(current_date.strftime("%B"))
            else:
                if current_date.strftime("%B") not in years_months[current_date.year]:
                    years_months[current_date.year].append(current_date.strftime("%B"))

        main_title = ""
        for i in years_months.keys():
            for q in years_months[i]:
                if len(years_months[i]) > 1:
                    if years_months[i].index(q) == 0:
                        main_title = f"{q}"
                    else:
                        main_title += f" - {q} {i}"
                elif len(years_months.keys()) > 1:
                    if len(main_title) == 0:
                        main_title = f"{q} {i}"
                    else:
                        main_title += f" - {q} {i}"
                else:
                    main_title = f"{q} {i}"

        self.calendarView.setHorizontalHeaderLabels([f"{days_of_week[0]} SUN", f"{days_of_week[1]} MON", f"{days_of_week[2]} TUE", f"{days_of_week[3]} WED", f"{days_of_week[4]} THU", f"{days_of_week[5]} FRI", f"{days_of_week[6]} SAT"])
        self.monthLabel.setText(main_title)
