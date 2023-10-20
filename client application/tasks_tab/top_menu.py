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
        self.buttons = []
        grid.setAlignment(Qt.AlignLeft)

        self.allTasksButton = QPushButton()
        self.allTasksButton.setText("All tasks (0)")
        self.allTasksButton.setFixedHeight(58)
        self.allTasksButton.setFixedWidth(85)
        self.allTasksButton.setProperty("topMenuButton", True)
        self.allTasksButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.buttons.append(self.allTasksButton)
        grid.addWidget(self.allTasksButton)
