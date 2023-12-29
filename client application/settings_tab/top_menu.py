from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class TopMenu(QMainWindow):
    def __init__(self, settingsTab):
        super().__init__()
        self.setContentsMargins(0, 0, 20, 0)
        self.setFixedHeight(58)
        self.setProperty("tasksTopMenu", True)
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        self.buttons = []
        self.settingsTab = settingsTab
        self.currentIndex = 0

        topLayout = QGridLayout(self.widget)
        self.leftWrapper = QScrollArea()
        self.leftWrapper.setFixedHeight(50)
        self.leftWrapper.setContentsMargins(0, 0, 0, 0)
        self.innerLeft = QWidget()
        self.leftWrapper.verticalScrollBar().hide()
        self.leftWrapper.verticalScrollBar().setEnabled(False)
        self.leftWrapper.horizontalScrollBar().hide()
        self.leftWrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.leftWrapper.setWidget(self.innerLeft)
        self.innerLeft.setFixedHeight(58)
        self.innerLeft.setContentsMargins(0, 0, 0, 0)
        topLayout.addWidget(self.leftWrapper, 0, 0)

        layout = QGridLayout(self.innerLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(4, 2)

        self.__add_button("Application", index=0)
        self.__add_button("Account", index=1)

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
        button.setFocusPolicy(Qt.NoFocus)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        if index is not None:
            button.clicked.connect(lambda: self.setTab(index))
        self.buttons.append(button)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.innerLeft.setFixedWidth(self.leftWrapper.width())

    def setTab(self, index: int):
        if self.currentIndex is not index:
            self.currentIndex = index
            for button in self.buttons:
                if button.property("selected"):
                    button.setProperty("selected", False)
                    button.setStyleSheet("")
            self.buttons[index].setProperty("selected", True)
            self.buttons[index].setStyleSheet("")
            self.settingsTab.bottomMenu.setTab(index)
        else:
            return False
