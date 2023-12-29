from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QScrollArea, QHeaderView, QTabWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap, QFont
from color_icon import color_pixmap
from PyQt5.QtCore import Qt, QSize
from qfluentwidgets import IconWidget, FluentIcon, InfoBarIcon, ProgressBar, PushButton
from config import edit_config

class ApplicationSettings(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 20, 0, 0)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignTop)
        self.themeButton = PushButton()
        self.parent = mainWindow
        if self.parent.is_dark:
            self.themeButton.setText("Set theme to Light mode")
            self.themeButton.setIcon(QIcon("icons/sun.png"))
        else:
            self.themeButton.setText("Set theme to Dark mode")
            self.themeButton.setIcon(QIcon("icons/moon.png"))
        self.themeButton.clicked.connect(self.toggleDarkmode)
        self.themeButton.setProperty("settings", True)
        self.themeButton.setFocusPolicy(Qt.NoFocus)
        self.themeButton.setIconSize(QSize(20, 20))
        self.themeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.grid.addWidget(self.themeButton)

        self.autoResizeColumnsButton = PushButton()
        if not self.parent.autoResizeColumns:
            self.autoResizeColumnsButton.setText("Enable auto resizing on Tasks table")
        else:
            self.autoResizeColumnsButton.setText("Disable auto resizing on Tasks table")
        self.autoResizeColumnsButton.clicked.connect(self.toggleAutoResize)
        self.autoResizeColumnsButton.setProperty("settings", True)
        self.autoResizeColumnsButton.setFocusPolicy(Qt.NoFocus)
        self.autoResizeColumnsButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.grid.addWidget(self.autoResizeColumnsButton)

    def toggleDarkmode(self):
        self.parent.toggleDarkmode()
        if self.parent.is_dark:
            self.themeButton.setText("Set theme to Light mode")
            self.themeButton.setIcon(QIcon("icons/sun.png"))
            edit_config("Settings.theme", '1')
        else:
            self.themeButton.setText("Set theme to Dark mode")
            self.themeButton.setIcon(QIcon("icons/moon.png"))
            edit_config("Settings.theme", '0')

    def toggleAutoResize(self):
        if self.parent.autoResizeColumns:
            self.parent.autoResizeColumns = False
            edit_config("Settings.auto_resize_columns", '0')
            self.autoResizeColumnsButton.setText("Enable auto resizing on Tasks table")
            self.parent.mainTabWidget.tasksTab.contentWindow.defaultColumnWidth()
        else:
            self.parent.autoResizeColumns = True
            self.autoResizeColumnsButton.setText("Disable auto resizing on Tasks table")
            self.parent.mainTabWidget.tasksTab.contentWindow.fixTableColumnWidth()
            edit_config("Settings.auto_resize_columns", '1')


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
