from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QGraphicsDropShadowEffect, QHeaderView, QAbstractItemView, QPushButton
from PyQt5.QtGui import QColor, QFont, QCursor
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
        self.ignore_datepicked = False
        self.monthLabel = QLabel("...")
        self.monthLabel.setProperty("calendarLabel", True)
        self.previousWeek = QPushButton()
        self.previousWeek.setText("◄")
        self.previousWeek.setFixedWidth(22)
        self.previousWeek.setFixedHeight(22)
        self.previousWeek.clicked.connect(self.toPreviousWeekFunction)
        self.previousWeek.setFocusPolicy(Qt.NoFocus)
        self.previousWeek.setCursor(QCursor(Qt.PointingHandCursor))
        self.previousWeek.setProperty("weekArrow", True)
        self.nextWeek = QPushButton()
        self.nextWeek.setText("►")
        self.nextWeek.setFixedWidth(22)
        self.nextWeek.setFixedHeight(22)
        self.nextWeek.setCursor(QCursor(Qt.PointingHandCursor))
        self.nextWeek.setProperty("weekArrow", True)
        self.nextWeek.clicked.connect(self.toNextWeekFunction)
        self.nextWeek.setFocusPolicy(Qt.NoFocus)
        self.calendarControllerGrid.addWidget(self.monthLabel, 0, 0)
        self.calendarControllerGrid.addWidget(self.previousWeek, 0, 1)
        self.calendarControllerGrid.addWidget(self.picker, 0, 2)
        self.calendarControllerGrid.addWidget(self.nextWeek, 0, 3)

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
        self.calendarView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.calendarView.setSelectionMode(QAbstractItemView.NoSelection)
        self.calendarView.setShowGrid(False)
        self.calendarView.horizontalHeader().sectionDoubleClicked.connect(self.focusColumn)
        self.calendarView.horizontalHeader().setStyleSheet("::section{border-right:none;padding-left:5px;padding-right:5px;}")
        self.calendarView.verticalHeader().setStyleSheet("::section{border:none;border-right:1px solid rgba(80,80,80,60);background:transparent;padding-bottom:27px;color:rgba(120,120,120,255);padding-left:5px;padding-right:5px;font-size:10px;}")
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


        self.picker.setDate(QDate().currentDate())

        self.calendarWindow.setGraphicsEffect(boxShadow)

    def focusColumn(self, column):
        self.ignore_datepicked = True
        self.picker.setDate(QDate(self.days_of_week[column]))
        self.ignore_datepicked = False
        self.selectedDate = self.days_of_week[column]
        for i in range(7):
            header_label = self.calendarView.horizontalHeaderItem(i)
            if column != i:
                font = header_label.font()
                font.setBold(False)
                font.setFamily("verdana")
                header_label.setFont(font)
            else:
                font = header_label.font()
                font.setBold(True)
                font.setFamily("verdana")
                header_label.setFont(font)
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
        if not self.ignore_datepicked:
            self.days_of_week = []
            years_months = {}
            self.selectedDate = date.toPyDate()
            column_index = int(self.selectedDate.strftime("%w"))
            sunday = self.selectedDate - timedelta(days=int(self.selectedDate.strftime("%w")))
            for i in range(7):
                header_label = self.calendarView.horizontalHeaderItem(i)
                if column_index != i:
                    font = header_label.font()
                    font.setBold(False)
                    font.setFamily("verdana")
                    header_label.setFont(font)
                else:
                    font = header_label.font()
                    font.setBold(True)
                    font.setFamily("verdana")
                    header_label.setFont(font)
                current_date = sunday + timedelta(days=i)
                self.days_of_week.append(current_date)
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

            self.calendarView.setHorizontalHeaderLabels([f"SUN\n{self.days_of_week[0].day}", f"MON\n{self.days_of_week[1].day}", f"TUE\n{self.days_of_week[2].day}", f"WED\n{self.days_of_week[3].day}", f"THU\n{self.days_of_week[4].day}", f"FRI\n{self.days_of_week[5].day}", f"SAT\n{self.days_of_week[6].day}"])
            self.monthLabel.setText(main_title)

    def toPreviousWeekFunction(self):
        self.picker.setDate(QDate(self.selectedDate - timedelta(days=7)))

    def toNextWeekFunction(self):
        self.picker.setDate(QDate(self.selectedDate + timedelta(days=7)))
