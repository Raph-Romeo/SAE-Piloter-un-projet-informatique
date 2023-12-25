from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from .top_menu import TopMenu
from .bottom_menu import BottomMenu


class TasksTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)

        self.topMenu = TopMenu(self)
        self.grid.addWidget(self.topMenu)

        self.contentWindow = BottomMenu(parent, self)
        self.contentWindow.setProperty("tasksContentWindow", True)
        self.grid.addWidget(self.contentWindow)

        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.topMenu.setGraphicsEffect(boxShadow)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.contentWindow.setGraphicsEffect(boxShadow)

    def update_tasks(self, tasks):
        self.contentWindow.set_tasks(tasks)
