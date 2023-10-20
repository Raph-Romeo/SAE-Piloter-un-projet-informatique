from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QSpacerItem, QSizePolicy
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

        topLayout = QGridLayout(self.widget)
        self.leftWrapper = QWidget()
        self.leftWrapper.setFixedHeight(58)
        self.leftWrapper.setContentsMargins(0, 0, 0, 0)
        self.leftWrapper.setMinimumWidth(420)
        topLayout.addWidget(self.leftWrapper, 0, 0)

        self.addTaskButton = QPushButton()
        self.addTaskButton.setProperty("addTaskButton", True)
        self.addTaskButton.setText("＋")
        self.addTaskButton.setFixedWidth(58)
        self.addTaskButton.setFixedHeight(28)
        self.addTaskButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.addTaskButton.setToolTip("Create new task")
        topLayout.addWidget(self.addTaskButton, 0, 1)

        layout = QGridLayout(self.leftWrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(4, 2)

        self.__add_button("All tasks (0)")
        self.__add_button("Expiring soon")
        self.__add_button("Incomplete")
        self.__add_button("Completed")

        self.buttons[0].setProperty("selected", True)

        for button in self.buttons:
            layout.addWidget(button, 0, self.buttons.index(button)+1)
            layout.setAlignment(button, Qt.AlignCenter)

        spacer_left = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer_right = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer_left, 0, 0)
        layout.addItem(spacer_right, 0, len(self.buttons)+1)

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

    def setTaskNumber(self, num: int):
        if num > 99:
            self.buttons[0].setText("All tasks (+99)")
        else:
            self.buttons[0].setText(f"All tasks ({str(num)})")
