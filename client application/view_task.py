import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
from datetime import datetime


def format_date(input_string):
    def ordinal_suffix(day):
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return str(day) + suffix

    try:
        # Parse the input string into a datetime object
        input_datetime = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")

        # Format the output string as "{day}th of {month} %Y"
        output_string = "{} of {} {}".format(
            ordinal_suffix(input_datetime.day),
            input_datetime.strftime("%B"),
            input_datetime.strftime("%Y")
        )

        return output_string
    except:
        return input_string


class ViewTask(MessageBoxBase):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.mainWindow = parent
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel(f'View task details [ {data["name"]} ]', self)
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

        self.statusLayout = QWidget()
        layout2 = QHBoxLayout(self.statusLayout)
        layout2.setSpacing(0)
        layout2.setContentsMargins(15, 0, 0, 0)

        self.taskName = QLabel(f"Task name: {data['name']}")
        self.taskTag = QLabel(f"Tag : {data['tag']} | Priority : {data['importance']} ⚠️")
        self.taskTag.setStyleSheet("font-size:14px;font-family:verdana;color:gray")
        self.taskName.setStyleSheet("font-size:18px;font-family:verdana;")
        status = ["incomplete", "completed"]
        self.completeCheckbox = CheckBox()
        if data['is_complete']:
            self.completeCheckbox.setChecked(True)
        self.completeCheckbox.setFixedWidth(40)
        self.status = QLabel(f"Task is {status[data['is_complete']]}")
        self.status.setStyleSheet("font-size:14px;font-family:verdana;color:gray")
        self.taskTag.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskUser = QLabel(f"Task is for user {data['user']['u']} ({data['user']['e']})")
        self.taskUser.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskDescription = QLabel(f"Description : ")
        self.taskDescription.setStyleSheet("font-size:14px;font-family:verdana;")
        self.taskDescriptionText = QTextEdit()
        self.descriptionSeparator = HorizontalSeparator()
        if data['description'] is not None:
            self.taskDescriptionText.setPlainText(data['description'])
        else:
            self.taskDescriptionText.setPlainText("")
            self.taskDescription.setHidden(True)
            self.taskDescriptionText.setHidden(True)
            self.descriptionSeparator.setHidden(True)
            self.taskDescriptionText.setPlaceholderText("Description")
        self.taskDescriptionText.setReadOnly(True)
        self.taskDescriptionText.setStyleSheet("margin-left:20px;")
        self.creation = QLabel(f"Created on the {format_date(data['creation_date'])}, by user {data['creator']['u']} ({data['creator']['e']})")
        self.creation.setStyleSheet("font-size:14px;font-family:verdana;")
        self.start_date = QLabel(f"Start date : {format_date(data['start_date'])} at {data['start_date'].split(' ')[1]}")
        self.start_date.setStyleSheet("font-size:14px;font-family:verdana;")
        if data['deadline'] != 'None':
            self.deadline = QLabel(f"Task must be completed before : {format_date(data['deadline'])} at {data['deadline'].split(' ')[1]}")
        else:
            self.deadline = QLabel()
            self.deadline.setHidden(True)
        self.deadline.setStyleSheet("font-size:14px;font-family:verdana;")

        layout1.addWidget(self.taskName)
        layout1.addWidget(self.taskTag)

        layout1.addWidget(self.statusLayout)
        layout2.addWidget(self.completeCheckbox)
        layout2.addWidget(self.status)

        layout1.addWidget(self.descriptionSeparator)
        layout1.addWidget(self.taskDescription)
        layout1.addWidget(self.taskDescriptionText)

        layout1.addWidget(HorizontalSeparator())

        layout1.addWidget(self.taskUser)
        layout1.addWidget(self.creation)

        layout1.addWidget(HorizontalSeparator())

        layout1.addWidget(self.start_date)
        layout1.addWidget(self.deadline)

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
