import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime

class AddFriendForm(MessageBoxBase):
    def __init__(self, parent, friends_tab):
        super().__init__(parent)
        self.mainWindow = parent
        self.friends_tab = friends_tab
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel(f'Add friend', self)
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

        l1 = QLabel("Account username : ")
        l1.setStyleSheet("font-size:12px;font-family:verdana;")

        self.friendNameInput = QLineEdit()
        self.friendNameInput.setPlaceholderText("Username")
        self.friendNameInput.setProperty("create_task_form", True)
        self.friendNameInput.returnPressed.connect(self.add_friend)
        self.friendNameInput.textChanged.connect(self.validateForm)

        self.confirmButton = PushButton()
        self.confirmButton.setText("Send friend request")
        self.confirmButton.setDisabled(True)
        self.confirmButton.setIcon(FluentIcon.SEND)
        self.confirmButton.clicked.connect(self.add_friend)
        self.confirmButton.setFixedWidth(350)

        self.viewLayout.addWidget(l1)
        self.viewLayout.addWidget(self.friendNameInput)
        self.viewLayout.addWidget(self.confirmButton)

        self.buttonGroup.setHidden(True)

    def cancelEvent(self, e):
        self.close()

    def add_friend(self):
        if len(self.friendNameInput.text()) >= 4:
            self.confirmButton.setDisabled(True)
            self.friendNameInput.setDisabled(True)
            self.friends_tab.send_friend_request(self.friendNameInput.text())
        else:
            InfoBar.warning(
                title="",
                content="Username must be at least 4 characters !",
                parent=self.mainWindow,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=5000
            )

    def validateForm(self):
        if len(self.friendNameInput.text()) >= 4:
            self.confirmButton.setDisabled(False)
        else:
            self.confirmButton.setDisabled(True)