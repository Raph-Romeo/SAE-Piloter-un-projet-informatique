from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class TopMenu(QMainWindow):
    def __init__(self, tasksTab):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(58)
        self.setProperty("tasksTopMenu", True)
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        self.buttons = []
        self.tasksTab = tasksTab
        self.currentIndex = 0

        topLayout = QGridLayout(self.widget)
        self.leftWrapper = QScrollArea()
        self.leftWrapper.setFixedHeight(50)
        self.leftWrapper.setContentsMargins(0, 0, 0, 0)
        self.innerLeft = QWidget()
        self.leftWrapper.verticalScrollBar().hide()
        self.leftWrapper.verticalScrollBar().setEnabled(False)
        self.leftWrapper.setWidget(self.innerLeft)
        self.innerLeft.setFixedHeight(58)
        self.innerLeft.setContentsMargins(0, 0, 0, 0)
        topLayout.addWidget(self.leftWrapper, 0, 0)

        self.addTaskButton = QPushButton()
        self.addTaskButton.setProperty("addTaskButton", True)
        self.addTaskButton.setText("＋")
        self.addTaskButton.setFixedWidth(38)
        self.addTaskButton.setFixedHeight(28)
        self.addTaskButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.addTaskButton.setToolTip("Create new task")
        topLayout.addWidget(self.addTaskButton, 0, 1)

        layout = QGridLayout(self.innerLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(4, 2)

        self.__add_button("All tasks (0)", index=0)
        self.__add_button("Expiring soon", index=1)
        self.__add_button("Incomplete", index=2)
        self.__add_button("Completed", index=3)

        self.buttons[0].setProperty("selected", True)

        for button in self.buttons:
            layout.addWidget(button, 0, self.buttons.index(button)+1)
            layout.setAlignment(button, Qt.AlignCenter)

        spacer_left = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer_right = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer_left, 0, 0)
        layout.addItem(spacer_right, 0, len(self.buttons)+1)

    def __add_button(self, text: str, h: int = 58, w: int = 120, index=None):
        button = QPushButton()
        button.setText(text)
        button.setFixedHeight(h)
        button.setFixedWidth(w)
        button.setProperty("topMenuButton", True)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        if index is not None:
            button.clicked.connect(lambda: self.setTab(index))
        self.buttons.append(button)

    def setTaskNumber(self, num: int):
        if num > 99:
            self.buttons[0].setText("All tasks (+99)")
        else:
            self.buttons[0].setText(f"All tasks ({str(num)})")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.widget.width() >= 560:
            self.innerLeft.setFixedWidth(self.leftWrapper.width() - 15)
            if not self.leftWrapper.horizontalScrollBar().isHidden():
                self.leftWrapper.horizontalScrollBar().hide()
                self.leftWrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            self.innerLeft.setFixedWidth(460)
            if self.leftWrapper.horizontalScrollBar().isHidden():
                self.leftWrapper.horizontalScrollBar().show()
                self.leftWrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def setTab(self, index: int):
        if self.currentIndex is not index:
            self.currentIndex = index
            for button in self.buttons:
                if button.property("selected"):
                    button.setProperty("selected", False)
                    button.setStyleSheet("")
            self.buttons[index].setProperty("selected", True)
            self.buttons[index].setStyleSheet("")
            self.tasksTab.contentWindow.searchBarQlineEdit.setText("")
            # Do the stuff
        else:
            return False