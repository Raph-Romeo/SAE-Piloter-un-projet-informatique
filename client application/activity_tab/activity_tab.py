from PyQt5.QtWidgets import QTabWidget, QMainWindow, QWidget, QGridLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ActivityTab(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 30)
        self.grid = QGridLayout(self)
        self.mainWindow = mainWindow

        self.activityTab = QMainWindow()
        self.activityTab.setProperty("tasksTopMenu", True)
        self.grid.addWidget(self.activityTab)

        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(20)
        boxShadow.setOffset(0)
        boxShadow.setColor(QColor(0, 0, 0, 60))
        self.activityTab.setGraphicsEffect(boxShadow)
