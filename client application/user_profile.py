import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import LineEdit, HyperlinkButton, CaptionLabel, MessageBoxBase, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime

class AccountProfile(MessageBoxBase):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.mainWindow = parent
        self.user = user
        if self.user.username == self.mainWindow.user.username:
            self.friend = False
        else:
            self.friend = True
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel(f'Viewing profile of {self.user.username}', self)
        self.titleLabel.setProperty("title", True)
        self.titleLabel.setStyleSheet("margin-left:0px;")
        self.closeButton = ToolButton()
        self.closeButton.setFixedHeight(40)
        self.closeButton.setProperty("create_task_form", True)
        self.closeButton.setFixedWidth(40)
        self.closeButton.clicked.connect(self.cancelEvent)
        self.closeButton.setIcon(FluentIcon.CLOSE)
        header_layout = QHBoxLayout(self.formHeader)
        header_layout.addWidget(self.titleLabel)
        header_layout.addWidget(self.closeButton)
        self.viewLayout.addWidget(self.formHeader)
        self.viewLayout.setAlignment(Qt.AlignLeft)

        l1 = QLabel(f"Username : {self.user.username}")
        l1.setStyleSheet("font-size:12px;font-family:verdana;")
        l2 = QLabel(f"First name : {self.user.first_name}")
        l2.setStyleSheet("font-size:12px;font-family:verdana;")
        l3 = QLabel(f"Last name : {self.user.last_name}")
        l3.setStyleSheet("font-size:12px;font-family:verdana;")
        l4 = QLabel(f"Email : {self.user.email}")
        l4.setStyleSheet("font-size:12px;font-family:verdana;")

        self.viewLayout.addWidget(l1)
        self.viewLayout.addWidget(l2)
        self.viewLayout.addWidget(l3)
        self.viewLayout.addWidget(l4)

        if self.friend:
            self.removeFriendButton = PushButton()
            self.removeFriendButton.setText("Unfriend")
            self.removeFriendButton.setDisabled(False)
            self.removeFriendButton.setIcon(FluentIcon.REMOVE)
            self.removeFriendButton.clicked.connect(self.remove_friend)
            self.removeFriendButton.setFixedWidth(350)
            self.viewLayout.addWidget(self.removeFriendButton)

        self.buttonGroup.setHidden(True)

    def cancelEvent(self, e):
        self.close()

    def remove_friend(self):
        self.mainWindow.unfriend(self.user.id)
        self.close()