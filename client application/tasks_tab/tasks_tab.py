from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from .top_menu import TopMenu


class TasksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()

        self.topMenu = TopMenu()
        self.grid.addWidget(self.topMenu)

        self.contentWindow = QWidget()
        self.contentWindow.setProperty("tasksContentWindow", True)
        self.grid.addWidget(self.contentWindow)

    def darkBoxShadows(self):
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(20, 20, 20))
        self.topMenu.setGraphicsEffect(boxShadow)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(20, 20, 20))
        self.contentWindow.setGraphicsEffect(boxShadow)

    def lightBoxShadows(self):
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(160, 160, 160))
        self.topMenu.setGraphicsEffect(boxShadow)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(160, 160, 160))
        self.contentWindow.setGraphicsEffect(boxShadow)