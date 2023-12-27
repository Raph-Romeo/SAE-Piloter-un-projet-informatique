import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime, timedelta

class ViewTask(MessageBoxBase):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.mainWindow = parent
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel(f'View task details > {data["name"]}', self)
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
        self.formInterface.setFixedWidth(620)
        self.formInterface.setFixedHeight(320)

        # PAGE 1 _________________________________________________

        self.formPage1 = QWidget()
        self.formPage1.setContentsMargins(0, 0, 0, 0)
        layout1 = QVBoxLayout(self.formPage1)
        layout1.setAlignment(Qt.AlignTop)

        self.taskName = QLabel(f"Task name: {data['name']}")
        self.taskName.setStyleSheet("font-size:18px;font-family:verdana;")
        status = ["incomplete ❌", "completed ✅"]
        self.status = QLabel(f"Task is {status[data['is_complete']]}")
        self.status.setStyleSheet("font-size:14px;font-family:verdana;color:gray")
        self.taskTag = QLabel(f"Task tag: {data['tag']}")
        self.taskTag.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskUser = QLabel(f"User : 👤 {data['user']['u']}")
        self.taskUser.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskDescription = QLabel(f"Description : ")
        self.taskDescription.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskDescriptionText = QTextEdit()
        if data['description'] is not None:
            self.taskDescriptionText.setPlainText(data['description'])
        else:
            self.taskDescriptionText.setPlainText("No description.")
        self.taskDescriptionText.setReadOnly(True)
        self.creation = QLabel(f"Created on : {data['creation_date']}, by user 👤 {data['creator']['u']}")
        self.creation.setStyleSheet("font-size:14px;font-family:verdana;")
        self.start_date = QLabel(f"Start date : {data['start_date']}")
        self.start_date.setStyleSheet("font-size:14px;font-family:verdana;")
        self.deadline = QLabel(f"Deadline : {data['deadline']}")
        self.deadline.setStyleSheet("font-size:14px;font-family:verdana;")

        layout1.addWidget(self.taskName)
        layout1.addWidget(self.status)

        layout1.addWidget(HorizontalSeparator())

        layout1.addWidget(self.taskTag)
        layout1.addWidget(self.taskUser)

        layout1.addWidget(HorizontalSeparator())

        layout1.addWidget(self.creation)
        layout1.addWidget(self.start_date)
        layout1.addWidget(self.deadline)

        layout1.addWidget(HorizontalSeparator())

        layout1.addWidget(self.taskDescription)
        layout1.addWidget(self.taskDescriptionText)

        # PAGE 3 END _________________________________________________

        self.formInterface.addWidget(self.formPage1)

        self.viewLayout.addWidget(self.formInterface)

        self.footer = QWidget()
        self.footer.setFixedHeight(60)
        footer_layout = QHBoxLayout(self.footer)
        self.backB = PushButton()
        self.backB.setText("BACK")
        self.backB.setDisabled(True)
        self.nextB = PushButton()
        self.nextB.setText("NEXT")
        self.backB.setIcon(FluentIcon.LEFT_ARROW)
        self.nextB.setIcon(FluentIcon.RIGHT_ARROW)
        footer_layout.addWidget(self.backB)
        footer_layout.addWidget(self.nextB)
        self.viewLayout.addWidget(self.footer)

        self.buttonGroup.setHidden(True)

    def cancelEvent(self, e):
        self.close()
