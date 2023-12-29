from PyQt5.QtWidgets import QTabWidget, QLabel, QTableWidget, QMainWindow, QHeaderView, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from qfluentwidgets import MessageBoxBase, IconWidget, TableWidget, InfoBarIcon, HorizontalSeparator, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, CalendarPicker, CheckBox, TimePicker, DatePicker, FluentIcon, ToolButton, ComboBox, InfoBar, InfoBarPosition
import json
from .add_friend_form import AddFriendForm
from .friend_request_menu import FriendRequestMenu


class Friend(QWidget):
    def __init__(self, username):
        super().__init__()
        # self.avatar = AvatarWidget()
        # self.avatar.setImage(user.profile_picture)
        # self.avatar.setRadius(12)
        # User avatar causes major lag to the application.
        self.icon = IconWidget(QIcon("icons/default.png"))
        self.icon.setFixedHeight(24)
        self.icon.setFixedWidth(24)
        self.username = QLabel(username)
        self.username.setStyleSheet("font-family:verdana;margin:0px;font-size:12px")
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 0, 0)
        # layout.addWidget(self.avatar)
        layout.addWidget(self.icon)
        layout.addWidget(self.username)


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
        friendsTabLayout.setContentsMargins(10, 5, 30, 0)
        self.friendsTab.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.friendsTab)

        self.topTitle = QLabel("All Friends")
        self.topTitle.setProperty("calendarLabel", True)
        friendsTabLayout.addWidget(self.topTitle, 0, 0)

        self.refreshFriendsButton = ToolButton()
        self.refreshFriendsButton.setIcon(FluentIcon.UPDATE)
        self.refreshFriendsButton.setToolTip("Refresh friends")
        self.refreshFriendsButton.clicked.connect(self.refresh_friends)
        friendsTabLayout.addWidget(self.refreshFriendsButton, 0, 1)

        self.requestsButton = PushButton()
        self.requestsButton.setText("Friend requests")
        self.requestsButton.setIcon(None)
        self.requestsButton.setFixedWidth(150)
        self.requestsButton.clicked.connect(self.init_friend_requests_menu)
        friendsTabLayout.addWidget(self.requestsButton, 0, 2)

        self.addFriendButton = PushButton()
        self.addFriendButton.setText("Add friend")
        self.addFriendButton.setIcon(FluentIcon.ADD)
        self.addFriendButton.setFixedWidth(120)
        self.addFriendButton.clicked.connect(self.init_add_friend_form)
        friendsTabLayout.addWidget(self.addFriendButton, 0, 3)

        self.noFriendsLabel = QLabel("You currently have no friends.")
        self.noFriendsLabel.setStyleSheet("font-family:verdana;font-size:14px;margin-top:20px;")
        self.noFriendsLabel.setAlignment(Qt.AlignCenter)
        self.noFriendsLabel.setHidden(True)
        friendsTabLayout.addWidget(self.noFriendsLabel, 1, 0, 1, 4)

        self.friendsTable = TableWidget()
        self.friendsTable.setColumnCount(2)
        self.friendsTable.setRowCount(0)
        self.friendsTable.setSelectionMode(QTableWidget.SingleSelection)
        self.friendsTable.setHorizontalHeaderLabels(["Username", "First name"])
        self.friendsTable.setWordWrap(False)

        self.friendsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.friendsTable.verticalHeader().setHidden(True)
        self.friendsTable.horizontalHeader().setHidden(True)
        self.friendsTable.doubleClicked.connect(self.friendDoubleClicked)

        friendsTabLayout.addWidget(self.friendsTable, 2, 0, 1, 4)

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
        username_label = Friend(username)
        username_label.setStyleSheet("font-family:verdana;font-size:12px;font-weight:bold")
        name_label = QLabel(f"{first_name} {last_name}")
        name_label.setStyleSheet("font-family:verdana;font-size:12px;font-style: italic;opacity:50%")
        row = self.friendsTable.rowCount()
        self.friendsTable.setRowCount(row + 1)
        self.friendsTable.setCellWidget(row, 0, username_label)
        self.friendsTable.setCellWidget(row, 1, name_label)

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
        if len(friend_list) == 0:
            self.noFriendsLabel.setHidden(False)
        else:
            self.noFriendsLabel.setHidden(True)
            self.friendsTable.resizeRowsToContents()
            self.friendsTable.resizeColumnToContents(0)
            self.friendsTable.setColumnWidth(0, self.friendsTable.columnWidth(0) + 5)

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
            InfoBar.info(title="", content=data["message"], parent=self.mainWindow, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
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

    def init_friend_requests_menu(self):
        message = json.dumps({"url": "/friend_request", "method": "GET", "token": self.mainWindow.user.auth_token})
        return self.mainWindow.init_send(message.encode(), self.build_friend_requests_menu)

    def build_friend_requests_menu(self, response):
        data = json.loads(response.decode())
        if data["status"] == 200:
            self.friend_request_menu = FriendRequestMenu(self.mainWindow, self, data["data"])
            self.friend_request_menu.exec()
        else:
            print(data)

    def accept_friend_request(self, request_id: int):
        message = json.dumps({"url": "/accept_friend_request", "method": "POST", "token": self.mainWindow.user.auth_token, "data": {"request_id": request_id}})
        return self.mainWindow.init_send(message.encode(), self.accept_friend_request_response)

    def accept_friend_request_response(self, response):
        data = json.loads(response.decode())
        if data["status"] == 200:
            InfoBar.info(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            self.mainWindow.update_friends()
            self.mainWindow.number_of_friend_requests -= 1
            self.set_friend_requests(self.mainWindow.number_of_friend_requests)
            return
        elif data["status"] == 400:
            InfoBar.error(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        elif data["status"] == 404:
            InfoBar.warning(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)

    def deny_friend_request(self, request_id: int):
        message = json.dumps({"url": "/deny_friend_request", "method": "POST", "token": self.mainWindow.user.auth_token, "data": {"request_id": request_id}})
        return self.mainWindow.init_send(message.encode(), self.deny_friend_request_response)

    def deny_friend_request_response(self, response):
        data = json.loads(response.decode())
        if data["status"] == 200:
            InfoBar.info(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            self.mainWindow.number_of_friend_requests -= 1
            self.set_friend_requests(self.mainWindow.number_of_friend_requests)
            return
        elif data["status"] == 400:
            InfoBar.error(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        elif data["status"] == 404:
            InfoBar.warning(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)

    def cancel_friend_request(self, request_id: int):
        message = json.dumps({"url": "/cancel_friend_request", "method": "POST", "token": self.mainWindow.user.auth_token, "data": {"request_id": request_id}})
        return self.mainWindow.init_send(message.encode(), self.cancel_friend_request_response)

    def cancel_friend_request_response(self, response):
        data = json.loads(response.decode())
        if data["status"] == 200:
            InfoBar.info(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            return
        elif data["status"] == 400:
            InfoBar.error(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        elif data["status"] == 404:
            InfoBar.warning(title="", content=data["message"], parent=self.mainWindow,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)

    def refresh_friends(self):
        InfoBar.info(title="", content="Refreshing friends...", parent=self.mainWindow, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=2000)
        self.refreshFriendsButton.setDisabled(True)
        self.mainWindow.update_friends()

    def friendDoubleClicked(self):
        self.mainWindow.view_account_profile(self.mainWindow.friends[self.friendsTable.selectedIndexes()[0].row()])