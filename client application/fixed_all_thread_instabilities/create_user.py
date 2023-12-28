import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime, timedelta
import re
import hashlib


class CreateUserForm(MessageBoxBase):
    def __init__(self, parent, return_func):
        super().__init__(parent)
        self.mainWindow = parent
        self.return_func = return_func
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel('Create User', self)
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
        layout1.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        usernamelabel = QLabel("Username")
        usernamelabel.setStyleSheet("font-size:12px;font-family:verdana;")
        self.usernameInput = QLineEdit()
        self.usernameInput.setProperty("create_task_form", True)
        self.usernameInput.setPlaceholderText('Username')
        emaillabel = QLabel("Email")
        emaillabel.setStyleSheet("font-size:12px;font-family:verdana;")

        self.emailInput = QLineEdit()
        self.emailInput.setProperty("create_task_form", True)
        self.emailInput.setPlaceholderText('example@domain.com')

        self.firstnameinput = QLineEdit()
        self.firstnameinput.setProperty("create_task_form", True)
        self.firstnameinput.setPlaceholderText("First name")

        self.lastnameinput = QLineEdit()
        self.lastnameinput.setProperty("create_task_form", True)
        self.lastnameinput.setPlaceholderText("Last name")

        account_details = QLabel("Account details")
        account_details.setStyleSheet("font-size:12px;font-family:verdana;")

        layout1.addWidget(usernamelabel)
        layout1.addWidget(self.usernameInput)
        layout1.addWidget(emaillabel)
        layout1.addWidget(self.emailInput)
        layout1.addWidget(account_details)
        layout1.addWidget(self.firstnameinput)
        layout1.addWidget(self.lastnameinput)

        # PAGE 2 _________________________________________________

        self.formPage2 = QWidget()
        self.formPage2.setContentsMargins(0, 0, 0, 0)
        layout2 = QGridLayout(self.formPage2)
        layout2.setAlignment(Qt.AlignTop)
        l1 = QLabel("Password")
        l1.setStyleSheet("font-size:12px;font-family:verdana;")
        layout2.addWidget(l1)

        self.passwordInput = QLineEdit("")
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setProperty("create_task_form", True)
        layout2.addWidget(self.passwordInput)

        l2 = QLabel("Confirm Password")
        l2.setStyleSheet("font-size:12px;font-family:verdana;")
        layout2.addWidget(l2)

        self.confirmPasswordInput = QLineEdit("")
        self.confirmPasswordInput.setPlaceholderText("Confirm password")
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)
        self.confirmPasswordInput.setProperty("create_task_form", True)
        layout2.addWidget(self.confirmPasswordInput)

        layout2.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # PAGE 3 _________________________________________________

        self.formPage3 = QWidget()
        self.formPage3.setContentsMargins(0, 0, 0, 0)
        layout3 = QGridLayout(self.formPage3)
        layout3.setAlignment(Qt.AlignTop)
        self.l4 = QPlainTextEdit("To create your account click on [CREATE USER].\n\nNOTE: You will not be able to change your username, first name and last name after this, so don't make any mistakes !")
        self.l4.setStyleSheet("margin:0;font-size:12px;font-family:verdana;opacity:0.8;border:none;padding:5px;padding-right:0px;")
        self.l4.setDisabled(True)
        layout3.addWidget(self.l4)

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
            if self.currentPage == 1:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                if len(self.usernameInput.text()) == 0 or len(self.emailInput.text()) == 0 or len(self.lastnameinput.text()) == 0 or len(self.firstnameinput.text()) == 0:
                    return self.formError("Please fill out all fields !")
                elif len(self.usernameInput.text()) < 4:
                    return self.formError("Minimum length for username is 4 !")
                elif not re.fullmatch(regex, self.emailInput.text()):
                    return self.formError("Invalid email !")
            elif self.currentPage == 2:
                if len(self.passwordInput.text()) == 0 or len(self.confirmPasswordInput.text()) == 0:
                    return self.formError("Please fill out both fields !")
                if self.passwordInput.text() != self.confirmPasswordInput.text():
                    return self.formError("Passwords don't match !")
                if len(self.passwordInput.text()) < 4:
                    return self.formError("Password length should be at least 4 characters !")
            self.currentPage += 1
            self.formInterface.setCurrentIndex(self.currentPage-1)
            self.backB.setDisabled(False)
            if self.currentPage == 3:
                self.nextB.setText("CREATE USER")
                self.nextB.setIcon(None)
        else:
            if self.currentPage == 3:
                self.nextB.setDisabled(True)
                username = self.usernameInput.text()
                password = hashlib.md5(self.passwordInput.text().encode()).hexdigest()
                email = self.emailInput.text()
                first_name = self.firstnameinput.text()
                last_name = self.lastnameinput.text()
                message = {"username": username, "password": password, "email": email, "first_name": first_name, "last_name": last_name}
                self.mainWindow.create_user(message, self.return_func)

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
