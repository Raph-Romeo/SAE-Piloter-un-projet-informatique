from PyQt5.QtWidgets import QTabWidget, QLabel, QMainWindow, QHeaderView, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from qfluentwidgets import PushButton, FluentIcon, TableWidget, IconWidget, InfoBarIcon

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

        self.topTitle = QLabel("All friends")
        self.topTitle.setProperty("calendarLabel", True)
        friendsTabLayout.addWidget(self.topTitle, 0, 0)

        self.notificationButton = PushButton()
        self.notificationButton.setText("Friend requests")
        self.notificationButton.setIcon(InfoBarIcon.WARNING)
        self.notificationButton.setFixedWidth(150)
        friendsTabLayout.addWidget(self.notificationButton, 0, 1)

        self.addFriendButton = PushButton()
        self.addFriendButton.setText("Add friend")
        self.addFriendButton.setIcon(FluentIcon.ADD)
        self.addFriendButton.setFixedWidth(120)
        friendsTabLayout.addWidget(self.addFriendButton, 0, 2)

        self.friendsTable = TableWidget()
        self.friendsTable.setColumnCount(3)
        self.friendsTable.setRowCount(0)
        self.friendsTable.setHorizontalHeaderLabels(["Username", "First name", "Last name"])

        self.addFriendToTable("Val74k", "Valentin", "Leconte")
        self.addFriendToTable("Sawix", "Elmir", "Batjari")

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
