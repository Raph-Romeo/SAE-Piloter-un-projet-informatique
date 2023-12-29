import sys
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime, timedelta

def user_format(users) -> list:
    user_list = []
    for user in users:
        user_list.append("👤 " + user)
    return user_list

class CreateTaskForm(MessageBoxBase):
    def __init__(self, parent, date=None):
        super().__init__(parent)
        self.mainWindow = parent
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel('Create task', self)
        self.titleLabel.setProperty("title", True)
        self.titleLabel.setStyleSheet("margin-left:0px;")
        self.closeButton = ToolButton()
        self.closeButton.setFixedHeight(40)
        self.closeButton.setProperty("create_task_form", True)
        self.closeButton.setFixedWidth(40)
        self.closeButton.clicked.connect(self.cancelEvent)
        self.closeButton.setIcon(FluentIcon.CLOSE)
        self.currentPage = 1
        header_layout = QHBoxLayout(self.formHeader)
        header_layout.addWidget(self.titleLabel)
        header_layout.addWidget(self.closeButton)
        self.viewLayout.addWidget(self.formHeader)

        self.formInterface = QStackedWidget()
        self.formInterface.setFixedWidth(320)
        self.formInterface.setFixedHeight(220)

        # PAGE 1 _________________________________________________

        self.formPage1 = QWidget()
        self.formPage1.setContentsMargins(0, 0, 0, 0)
        layout1 = QVBoxLayout(self.formPage1)
        self.taskName = QLineEdit()
        self.taskName.setProperty("create_task_form", True)
        self.taskName.setPlaceholderText('Task name')
        self.taskTag = QLineEdit()
        self.taskTag.setProperty("create_task_form", True)
        self.taskTag.setPlaceholderText('Task tag')
        self.taskDescription = QTextEdit()
        self.taskDescription.setProperty("create_task_form", True)
        self.taskDescription.setPlaceholderText('Task description')

        layout1.addWidget(self.taskName)
        layout1.addWidget(self.taskTag)
        layout1.addWidget(self.taskDescription)

        # PAGE 2 _________________________________________________

        self.formPage2 = QWidget()
        self.formPage2.setContentsMargins(0, 0, 0, 0)
        layout2 = QGridLayout(self.formPage2)
        layout2.setAlignment(Qt.AlignTop)
        l1 = QLabel("Task date")
        l1.setStyleSheet("font-size:12px;font-family:verdana;")
        self.startDatePicker = CalendarPicker()
        self.startDatetimePicker = TimePicker()
        self.deadlinePicker = CalendarPicker()
        self.deadlineTimePicker = TimePicker()
        if date is None:
            self.startDatePicker.setDate(QDate().currentDate())
            self.deadlinePicker.setDate(QDate().currentDate())

            self.startDatetimePicker.setTime(QTime(datetime.now().hour, datetime.now().minute, 0))
            self.deadlineTimePicker.setTime(QTime(datetime.now().hour, datetime.now().minute, 0))
        else:
            self.startDatePicker.setDate(QDate(date[0]))
            self.deadlinePicker.setDate(QDate(date[0]))

            self.startDatetimePicker.setTime(QTime(date[1], 0, 0))
            self.deadlineTimePicker.setTime(QTime(date[1], 0, 0))

        self.deadlineToggle = CheckBox()
        self.deadlineToggle.toggled.connect(self.toggle_deadline)
        self.deadlineCheckBoxLabel = QLabel("Include deadline")
        self.deadlineCheckBoxLabel.setStyleSheet("margin-left:30px;padding:0;font-family:verdana;font-size:12px")
        self.deadlinePicker.dateChanged.connect(self.changedDate)
        self.startDatePicker.dateChanged.connect(self.changedDate)
        self.deadlineTimePicker.timeChanged.connect(self.changeTime)
        self.startDatetimePicker.timeChanged.connect(self.changeTime)
        self.deadlineTimePicker.setHidden(True)
        self.deadlinePicker.setHidden(True)
        l2 = QLabel("Time")
        l2.setStyleSheet("font-size:12px;font-family:verdana;")
        self.l3 = QLabel("Time")
        self.l3.setStyleSheet("font-size:12px;font-family:verdana;")
        self.l3.setHidden(True)

        layout2.addWidget(l1, 0, 0, 1, 2)
        layout2.addWidget(self.startDatePicker, 1, 0, 1, 2)
        layout2.addWidget(self.startDatetimePicker, 2, 1, 1, 1)
        layout2.addWidget(l2, 2, 0, 1, 1)
        layout2.addWidget(self.deadlineCheckBoxLabel, 3, 0, 1, 2)
        layout2.addWidget(self.deadlineToggle, 3, 0, 1, 1)
        layout2.addWidget(self.deadlinePicker, 4, 0, 1, 2)
        layout2.addWidget(self.l3, 5, 0, 1, 1)
        layout2.addWidget(self.deadlineTimePicker, 5, 1, 1, 1)

        # PAGE 3 _________________________________________________

        self.formPage3 = QWidget()
        self.formPage3.setContentsMargins(0, 0, 0, 0)
        layout3 = QGridLayout(self.formPage3)
        layout3.setAlignment(Qt.AlignTop)
        l1 = QLabel("Task user")
        l1.setStyleSheet("font-size:12px;font-family:verdana;")
        self.selectUser = ComboBox()
        self.users = [self.mainWindow.user.username]
        self.selectUser.addItems(user_format(self.users))
        l2 = QLabel("Task priority")
        l2.setStyleSheet("font-size:12px;font-family:verdana;")
        self.selectImportance = ComboBox()
        self.selectImportance.addItems(['1', '2', '3'])
        l3 = QLabel("Share with friends")
        l3.setStyleSheet("font-size:12px;font-family:verdana;")
        self.l4 = QPlainTextEdit("Your friends will be able to see your task in their activity feed. They will also be updated on your task's status.")
        self.l4.setStyleSheet("margin:0;font-size:12px;font-family:verdana;opacity:0.8;border:none;padding:5px;padding-right:0px;")
        self.l4.setHidden(True)
        self.l4.setDisabled(True)
        self.publicCheckbox = CheckBox()
        self.publicCheckbox.toggled.connect(self.publicCheckboxEvent)
        layout3.addWidget(l1, 0, 0, 1, 1)
        layout3.addWidget(self.selectUser, 0, 1, 1, 1)
        layout3.addWidget(l2, 1, 0, 1, 1)
        layout3.addWidget(self.selectImportance, 1, 1, 1, 1)
        layout3.addWidget(l3, 2, 0, 1, 1)
        layout3.addWidget(self.publicCheckbox, 2, 1, 1, 1)
        layout3.addWidget(self.l4, 3, 0, 1, 2)

        # PAGE 3 END _________________________________________________

        self.formInterface.addWidget(self.formPage1)
        self.formInterface.addWidget(self.formPage2)
        self.formInterface.addWidget(self.formPage3)

        self.viewLayout.addWidget(self.formInterface)

        self.footer = QWidget()
        self.footer.setFixedHeight(60)
        footer_layout = QHBoxLayout(self.footer)
        self.backB = PushButton()
        self.backB.setText("BACK")
        self.backB.setDisabled(True)
        self.nextB = PushButton()
        self.nextB.setText("NEXT")
        self.nextB.clicked.connect(self.nextPage)
        self.backB.clicked.connect(self.previousPage)
        self.backB.setIcon(FluentIcon.LEFT_ARROW)
        self.nextB.setIcon(FluentIcon.RIGHT_ARROW)
        footer_layout.addWidget(self.backB)
        footer_layout.addWidget(self.nextB)
        self.viewLayout.addWidget(self.footer)
        self.buttonGroup.setHidden(True)

    def toggle_deadline(self, e):
        if self.deadlineToggle.isChecked():
            self.deadlineTimePicker.setHidden(False)
            self.deadlinePicker.setHidden(False)
            self.l3.setHidden(False)
        else:
            self.deadlineTimePicker.setHidden(True)
            self.deadlinePicker.setHidden(True)
            self.l3.setHidden(True)

    def cancelEvent(self, e):
        self.close()

    def nextPage(self):
        if self.currentPage <= 2:
            self.currentPage += 1
            self.formInterface.setCurrentIndex(self.currentPage-1)
            self.backB.setDisabled(False)
            if self.currentPage == 3:
                self.nextB.setText("CREATE TASK")
                self.nextB.setIcon(None)
        else:
            if self.currentPage == 3:
                self.nextB.setDisabled(True)
                if self.form_is_valid():
                    task_name = self.taskName.text()
                    task_tag = self.taskTag.text()
                    if len(self.taskDescription.toPlainText()) > 0:
                        task_description = self.taskDescription.toPlainText()
                    else:
                        task_description = None
                    start_date = self.startDatePicker.getDate().toPyDate()
                    start_date = datetime(start_date.year, start_date.month, start_date.day, self.startDatetimePicker.getTime().hour(), self.startDatetimePicker.getTime().minute())
                    if self.deadlineToggle.isChecked():
                        deadline = self.deadlinePicker.getDate().toPyDate()
                        deadline = datetime(deadline.year, deadline.month, deadline.day, self.deadlineTimePicker.getTime().hour(), self.deadlineTimePicker.getTime().minute())
                    else:
                        deadline = None
                    user = self.users[self.selectUser.currentIndex()]
                    message = {"name": task_name, "tag": task_tag, "description": task_description,
                               "start_date": str(start_date), "deadline": str(deadline), "user": user, "public": self.publicCheckbox.isChecked(), "importance": (self.selectImportance.currentIndex() + 1)}
                    self.mainWindow.create_task(message)
                else:
                    self.nextB.setDisabled(False)

    def form_is_valid(self) -> bool:
        if len(self.taskName.text()) == 0 or len(self.taskTag.text()) == 0:
            self.formError("You must fill out all fields.")
            return False
        elif self.deadlineToggle.isChecked():
            if self.startDatePicker.getDate().toPyDate() == self.deadlinePicker.getDate().toPyDate():
                if self.startDatetimePicker.getTime().hour() == self.deadlineTimePicker.getTime().hour():
                    if self.startDatetimePicker.getTime().minute() == self.deadlineTimePicker.getTime().minute():
                        self.formError("Deadline date and time cannot be equal to start date.")
                        return False
        return True

    def previousPage(self):
        if self.currentPage > 1:
            self.currentPage -= 1
            self.formInterface.setCurrentIndex(self.currentPage-1)
            if self.currentPage == 1:
                self.backB.setDisabled(True)
            elif self.currentPage == 2:
                self.nextB.setText("NEXT")
                self.nextB.setIcon(FluentIcon.RIGHT_ARROW)

    def warning(self):
        InfoBar.warning(
            title="Invalid deadline",
            content="Deadline date cannot be inferior to start date!",
            parent=self.mainWindow,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000
        )

    def formError(self, msg):
        InfoBar.error(
            title="Form is incomplete",
            content=msg,
            parent=self.mainWindow,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000
        )

    def changedDate(self, v):
        try:
            if self.deadlinePicker.getDate().toPyDate() < self.startDatePicker.getDate().toPyDate():
                self.deadlinePicker.setDate(self.startDatePicker.getDate())
                if self.deadlineToggle.isChecked():
                    self.warning()
                if self.startDatetimePicker.getTime() is not None and self.deadlineTimePicker.getTime() is not None:
                    if self.startDatetimePicker.getTime().hour() > self.deadlineTimePicker.getTime().hour():
                        self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                    elif self.startDatetimePicker.getTime().hour() == self.deadlineTimePicker.getTime().hour():
                        if self.startDatetimePicker.getTime().minute() > self.deadlineTimePicker.getTime().minute():
                            self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                    else:
                        return True
                return True
            elif self.deadlinePicker.getDate().toPyDate() == self.startDatePicker.getDate().toPyDate():
                if self.startDatetimePicker.getTime() is not None and self.deadlineTimePicker.getTime() is not None:
                    if self.startDatetimePicker.getTime().hour() > self.deadlineTimePicker.getTime().hour():
                        self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                        if self.deadlineToggle.isChecked():
                            self.warning()
                    elif self.startDatetimePicker.getTime().hour() == self.deadlineTimePicker.getTime().hour():
                        if self.startDatetimePicker.getTime().minute() > self.deadlineTimePicker.getTime().minute():
                            self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                            if self.deadlineToggle.isChecked():
                                self.warning()
                    return True
        except:
            return True

    def changeTime(self, v):
        try:
            if self.startDatePicker.getDate() is not None and self.deadlinePicker.getDate() is not None:
                if self.deadlinePicker.getDate().toPyDate() == self.startDatePicker.getDate().toPyDate():
                    if self.startDatetimePicker.getTime().hour() > self.deadlineTimePicker.getTime().hour():
                        self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                        if self.deadlineToggle.isChecked():
                            self.warning()
                    elif self.startDatetimePicker.getTime().hour() == self.deadlineTimePicker.getTime().hour():
                        if self.startDatetimePicker.getTime().minute() > self.deadlineTimePicker.getTime().minute():
                            self.deadlineTimePicker.setTime(self.startDatetimePicker.getTime())
                            if self.deadlineToggle.isChecked():
                                self.warning()
        except:
            return


    def publicCheckboxEvent(self, v):
        if v:
            self.l4.setHidden(False)
        else:
            self.l4.setHidden(True)
