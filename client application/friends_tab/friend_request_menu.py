import sys

from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView, QApplication, QTableWidget, QWidget, QAbstractItemView, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QStackedWidget, QVBoxLayout, QLabel, QGridLayout, QPlainTextEdit
import json
from qfluentwidgets import MessageBoxBase, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition, TableWidget
from datetime import datetime


class RequestButton(ToolButton):
    def __init__(self, request_id, row, func):
        super().__init__()
        self.request_id = request_id
        self.row = row
        self.func = func

    def mouseReleaseEvent(self, event):
        if event.button() == 1:  # Left mouse button
            self.func(self.request_id, self.row)
        super().mousePressEvent(event)


class FriendRequestMenu(MessageBoxBase):
    def __init__(self, parent, friends_tab, data):
        super().__init__(parent)
        self.mainWindow = parent
        self.friends_tab = friends_tab
        self.friendRequests = data["friend_requests"]
        self.pendingRequests = data["pending_requests"]
        self.formHeader = QWidget()
        self.titleLabel = SubtitleLabel(f'Friend requests', self)
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

        if len(self.friendRequests) > 0:
            l1 = QLabel("Friend requests : ")
            l1.setStyleSheet("font-size:12px;font-family:verdana;")
            self.viewLayout.addWidget(l1)
            self.friendRequestsTable = TableWidget()
            self.friendRequestsTable.setColumnCount(3)
            self.friendRequestsTable.verticalHeader().setHidden(True)
            self.friendRequestsTable.horizontalHeader().setHidden(True)
            self.friendRequestsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.friendRequestsTable.setSelectionMode(QTableWidget.SingleSelection)
            self.friendRequestsTable.setFixedWidth(400)
            self.friendRequestsTable.setColumnWidth(1, 30)
            self.friendRequestsTable.setColumnWidth(2, 30)
            buttons = []
            for request in self.friendRequests:
                row = self.friendRequestsTable.rowCount()
                self.friendRequestsTable.setRowCount(row + 1)
                username_label = QLabel(request["u"])
                username_label.setStyleSheet("font-size:12px;font-family:verdana;")
                self.friendRequestsTable.setCellWidget(row, 0, username_label)
                button = RequestButton(request_id=request["request_id"], row=row, func=self.accept_request)
                button.setFixedWidth(30)
                button.setFixedHeight(60)
                button.setIcon(FluentIcon.ACCEPT)
                self.friendRequestsTable.setCellWidget(row, 1, button)
                button = RequestButton(request_id=request["request_id"], row=row, func=self.deny_request)
                button.setFixedWidth(30)
                button.setFixedHeight(60)
                button.setIcon(FluentIcon.CLOSE)
                self.friendRequestsTable.setCellWidget(row, 2, button)
            self.viewLayout.addWidget(self.friendRequestsTable)
        else:
            l1 = QLabel("You have no friend requests.")
            l1.setStyleSheet("font-size:12px;font-family:verdana;")
            self.viewLayout.addWidget(l1)


        if len(self.pendingRequests) > 0:
            l2 = QLabel("Pending requests : ")
            l2.setStyleSheet("font-size:12px;font-family:verdana;")
            self.viewLayout.addWidget(l2)
            self.pendingRequestsTable = TableWidget()
            self.pendingRequestsTable.setColumnCount(2)
            self.pendingRequestsTable.verticalHeader().setHidden(True)
            self.pendingRequestsTable.horizontalHeader().setHidden(True)
            self.pendingRequestsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.pendingRequestsTable.setFixedWidth(400)
            self.pendingRequestsTable.setSelectionMode(QTableWidget.SingleSelection)
            self.pendingRequestsTable.setColumnWidth(1, 30)
            for request in self.pendingRequests:
                row = self.pendingRequestsTable.rowCount()
                self.pendingRequestsTable.setRowCount(row + 1)
                username_label = QLabel(request["u"])
                username_label.setStyleSheet("font-size:12px;font-family:verdana;")
                self.pendingRequestsTable.setCellWidget(row, 0, username_label)
                button = RequestButton(request_id=request["request_id"], row=row, func=self.cancel_request)
                button.setFixedWidth(30)
                button.setFixedHeight(60)
                button.setIcon(FluentIcon.CLOSE)
                self.pendingRequestsTable.setCellWidget(row, 1, button)
            self.viewLayout.addWidget(self.pendingRequestsTable)
        else:
            l2 = QLabel("You have no pending requests.")
            l2.setStyleSheet("font-size:12px;font-family:verdana;")
            self.viewLayout.addWidget(l2)
        self.buttonGroup.setHidden(True)

    def cancelEvent(self, e):
        self.close()

    def cancel_request(self, request_id, row):
        self.pendingRequestsTable.setRowHidden(row, True)
        self.friends_tab.cancel_friend_request(request_id)

    def accept_request(self, request_id, row):
        self.friendRequestsTable.setRowHidden(row, True)
        self.friends_tab.accept_friend_request(request_id)

    def deny_request(self, request_id, row):
        self.friendRequestsTable.setRowHidden(row, True)
        self.friends_tab.deny_friend_request(request_id)
