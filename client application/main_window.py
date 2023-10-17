import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taskmaster pro")
        self.setProperty("MainWindow", True)
        self.resize(780, 534)
        self.setMinimumSize(520, 274)
        self.is_dark = False
        self.mainTabWidget = QWidget()
        grid = QGridLayout()
        grid.setContentsMargins(1, 28, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)
        self.titlebar = QWidget()
        self.titlebar.setFixedHeight(46)
        self.__navbar = QWidget()
        self.__navbar.setFixedWidth(148)
        grid.addWidget(self.titlebar, 0, 1)
        grid.addWidget(self.__navbar, 0, 0, 2, 1)
        grid.addWidget(self.mainTabWidget, 1, 1, 1, 1)
