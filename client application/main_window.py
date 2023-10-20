import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from stylesheets import dark_style_sheet, light_style_sheet
from navbar import MainNavbar
from tab_widgets import MainTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taskmaster PRO")
        self.setWindowIcon(QIcon('icons/taskmasterpro.png'))
        self.resize(780, 500)
        self.setMinimumSize(520, 240)
        self.is_dark = False
        self.mainTabWidget = MainTabWidget()
        grid = QGridLayout()
        widget = QWidget()
        widget.setLayout(grid)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setCentralWidget(widget)
        self.titlebar = QWidget()
        self.titlebar.setFixedHeight(56)
        self.__navbar = MainNavbar(self.mainTabWidget, self)
        self.__navbar.setFixedWidth(148)
        if self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()
        grid.addWidget(self.titlebar, 0, 1)
        grid.addWidget(self.__navbar, 0, 0, 2, 1)
        grid.addWidget(self.mainTabWidget, 1, 1, 1, 1)

    def toggleDarkmode(self):
        if not self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()

    def setDarkMode(self):
        if sys.platform == "win32":
            import pywinstyles
            pywinstyles.apply_style(self, "dark")
        self.setStyleSheet(dark_style_sheet)
        self.is_dark = True
        self.__navbar.darkModeIcons()

    def setLightMode(self):
        if sys.platform == "win32":
            import pywinstyles
            pywinstyles.apply_style(self, "light")
        self.setStyleSheet(light_style_sheet)
        self.is_dark = False
        self.__navbar.lightModeIcons()