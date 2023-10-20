from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class TopMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(58)
        self.setProperty("tasksTopMenu", True)
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        grid = QGridLayout(self.widget)
        grid.setSpacing(0)
        self.setCentralWidget(self.widget)
        grid.setAlignment(Qt.AlignLeft)
