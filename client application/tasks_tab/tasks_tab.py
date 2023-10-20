from PyQt5.QtWidgets import QTabWidget, QMainWindow, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor


class TasksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()

        self.topMenu = QMainWindow()
        self.topMenu.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.topMenu)

        self.contentWindow = QMainWindow()
        self.contentWindow.setProperty("tasksContentWindow", True)
        self.grid.addWidget(self.contentWindow)