from PyQt5.QtWidgets import QTabWidget, QLabel, QMainWindow, QHeaderView, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from qfluentwidgets import MessageBoxBase, TableWidget, InfoBarIcon, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
import json
from .add_friend_form import AddFriendForm

class FriendsTab(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 30)
        self.grid = QGridLayout(self)
        self.mainWindow = mainWindow

        self.friendsTab = QMainWindow()
        friends_tab_widget = QWidget()
        self.friendsTab.setCentralWidget(friends_tab_widget)
        friendsTabLayout = QGridLayout(friends_tab_widget)
        friendsTabLayout.setAlignment(Qt.AlignTop)
        friendsTabLayout.setContentsMargins(10, 20, 30, 0)
        self.friendsTab.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.friendsTab)

        self.topTitle = QLabel("All Friends")
        self.topTitle.setProperty("calendarLabel", True)
        friendsTabLayout.addWidget(self.topTitle, 0, 0)

        self.requestsButton = PushButton()
        self.requestsButton.setText("Friend requests")
        self.requestsButton.setIcon(None)
        self.requestsButton.setFixedWidth(150)
        # self.requestsButton.clicked.connect(OPEN FRIEND REQUEST MENU)
        friendsTabLayout.addWidget(self.requestsButton, 0, 1)

        self.addFriendButton = PushButton()
        self.addFriendButton.setText("Add friend")
        self.addFriendButton.setIcon(FluentIcon.ADD)
        self.addFriendButton.setFixedWidth(120)
        self.addFriendButton.clicked.connect(self.init_add_friend_form)
        friendsTabLayout.addWidget(self.addFriendButton, 0, 2)

        self.friendsTable = TableWidget()
        self.friendsTable.setColumnCount(3)
        self.friendsTable.setRowCount(0)
        self.friendsTable.setHorizontalHeaderLabels(["Username", "First name", "Last name"])
        self.friendsTable.setWordWrap(False)

        self.friendsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.friendsTable.verticalHeader().setHidden(True)

        friendsTabLayout.addWidget(self.friendsTable, 1, 0, 1, 3)

        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.friendsTab.setGraphicsEffect(boxShadow)

    def addFriendToTable(self, username, first_name, last_name):
        if username is None:
            username = "null"
        if first_name is None:
            first_name = "null"
        if last_name is None:
            last_name = "null"
        username_label = QLabel(username)
        username_label.setStyleSheet("font-family:verdana;font-size:12px;font-weight:bold")
        first_name_label = QLabel(first_name)
        first_name_label.setStyleSheet("font-family:verdana;font-size:12px;")
        last_name_label = QLabel(last_name)
        last_name_label.setStyleSheet("font-family:verdana;font-size:12px;")
        row = self.friendsTable.rowCount()
        self.friendsTable.setRowCount(row + 1)
        self.friendsTable.setCellWidget(row, 0, username_label)
        self.friendsTable.setCellWidget(row, 1, first_name_label)
        self.friendsTable.setCellWidget(row, 2, last_name_label)

    def set_friend_requests(self, num):
        if num > 0:
            self.requestsButton.setIcon(InfoBarIcon.WARNING)
            self.requestsButton.setFixedWidth(170)
            self.requestsButton.setText(f"Friend requests ({num})")
        else:
            self.requestsButton.setFixedWidth(150)
            self.requestsButton.setIcon(None)
            self.requestsButton.setText("Friend requests")

    def set_friends(self, friend_list):
        self.friendsTable.clearContents()
        self.friendsTable.setRowCount(0)
        for friend in friend_list:
            self.addFriendToTable(friend.username, friend.first_name, friend.last_name)

    def clear_friends(self):
        self.friendsTable.clearContents()
        self.friendsTable.setRowCount(0)
        self.set_friend_requests(0)

    def init_add_friend_form(self):
        self.add_friend_form = AddFriendForm(self.mainWindow, self)
        self.add_friend_form.exec()

    def send_friend_request(self, username: str):
        message = json.dumps({"url": "/friend_request", "method": "POST", "token": self.mainWindow.user.auth_token, "data": {"username": username}})
        return self.mainWindow.init_send(message.encode(), self.send_friend_request_response)

    def send_friend_request_response(self, response):
        data = json.loads(response.decode())
        if data["status"] == 200:
            InfoBar.info(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            if data["message"] == "Friend request accepted !":
                self.mainWindow.update_friends()
                self.mainWindow.number_of_friend_requests -= 1
                self.set_friend_requests(self.mainWindow.number_of_friend_requests)
            if self.add_friend_form is not None and self.add_friend_form.isActiveWindow():
                self.add_friend_form.close()
            return
        elif data["status"] == 400:
            InfoBar.error(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        elif data["status"] == 404:
            InfoBar.warning(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        if self.add_friend_form is not None and self.add_friend_form.isActiveWindow():
            self.add_friend_form.confirmButton.setDisabled(False)
            self.add_friend_form.friendNameInput.setDisabled(False)

