import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from tab_widgets import MainTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taskmaster PRO")
        self.resize(780, 500)
        self.setMinimumSize(520, 240)
        self.mainTabWidget = MainTabWidget()
        grid = QGridLayout()
        widget = QWidget()
        widget.setLayout(grid)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setCentralWidget(widget)
        grid.addWidget(self.mainTabWidget)