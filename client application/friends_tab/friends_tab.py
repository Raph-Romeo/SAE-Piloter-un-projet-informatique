from PyQt5.QtWidgets import QTabWidget, QLabel, QMainWindow, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

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
        friendsTabLayout.setContentsMargins(10, 26, 20, 0)
        self.friendsTab.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.friendsTab)

        self.monthLabel = QLabel("All friends")
        self.monthLabel.setProperty("calendarLabel", True)

        friendsTabLayout.addWidget(self.monthLabel)

        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.friendsTab.setGraphicsEffect(boxShadow)
