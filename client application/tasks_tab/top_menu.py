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
        self.setCentralWidget(self.widget)
        self.buttons = []

        layout = QGridLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(4, 2)

        self.__add_button("All tasks (0)")
        self.__add_button("Button 2")
        self.__add_button("Button 3")
        self.__add_button("Button 4")

        for button in self.buttons:
            layout.addWidget(button, 0, self.buttons.index(button))

    def __add_button(self, text: str, h: int = 58, w: int = 120, function=None):
        button = QPushButton()
        button.setText(text)
        button.setFixedHeight(h)
        button.setFixedWidth(w)
        button.setProperty("topMenuButton", True)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        if function is not None:
            button.clicked.connect(function)
        self.buttons.append(button)
