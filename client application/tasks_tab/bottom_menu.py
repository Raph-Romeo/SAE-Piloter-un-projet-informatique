from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class BottomMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setProperty("tasksTopMenu", True)
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)


    def generate_task(self, text: str, h: int = 58, w: int = 120, function=None):
        button = QPushButton()
        button.setText(text)
        button.setFixedHeight(h)
        button.setFixedWidth(w)
        button.setProperty("topMenuButton", True)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        if function is not None:
            button.clicked.connect(function)
        self.buttons.append(button)
