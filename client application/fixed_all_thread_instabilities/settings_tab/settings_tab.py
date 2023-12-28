from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .top_menu import TopMenu
from .bottom_menu import BottomMenu


class SettingsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)

        self.topMenu = TopMenu(self)
        self.grid.addWidget(self.topMenu)

        self.bottomMenu = BottomMenu(parent)
        self.bottomMenu.setProperty("tasksContentWindow", True)
        self.grid.addWidget(self.bottomMenu)

        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.topMenu.setGraphicsEffect(boxShadow)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.bottomMenu.setGraphicsEffect(boxShadow)
