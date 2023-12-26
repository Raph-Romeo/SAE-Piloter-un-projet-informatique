from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QScrollArea, QHeaderView, QTabWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap, QFont
from color_icon import color_pixmap
from PyQt5.QtCore import Qt, QSize
from qfluentwidgets import IconWidget, FluentIcon, InfoBarIcon, ProgressBar

class ApplicationSettings(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()
        self.parent = mainWindow
        if self.parent.is_dark:
            self.button.setText("Set theme to Light mode")
            self.button.setIcon(QIcon("icons/sun.png"))
        else:
            self.button.setText("Set theme to Dark mode")
            self.button.setIcon(QIcon("icons/moon.png"))
        self.button.clicked.connect(self.toggleDarkmode)
        self.button.setProperty("settings", True)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.setIconSize(QSize(20,20))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.grid.addWidget(self.button)

    def toggleDarkmode(self):
        self.parent.toggleDarkmode()
        if self.parent.is_dark:
            self.button.setText("Set theme to Light mode")
            self.button.setIcon(QIcon("icons/sun.png"))
        else:
            self.button.setText("Set theme to Dark mode")
            self.button.setIcon(QIcon("icons/moon.png"))



class AccountSettings(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()
        self.parent = mainWindow
        self.button.setText("Sign out")
        self.button.clicked.connect(self.parent.logout)
        self.button.setProperty("signout", True)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.setIconSize(QSize(20, 20))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.grid.addWidget(self.button)


class BottomMenu(QMainWindow):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 0, 20, 21)
        self.setProperty("tasksTopMenu", True)
        self.parent = mainWindow
        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(ApplicationSettings(mainWindow), "Application settings")
        self.tabwidget.addTab(AccountSettings(mainWindow), "Account settings")
        self.setCentralWidget(self.tabwidget)
        self.tabwidget.tabBar().hide()


    def setTab(self, value: int) -> None:
        self.tabwidget.setCurrentIndex(value)
        return
