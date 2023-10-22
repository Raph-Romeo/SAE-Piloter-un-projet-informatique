from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QGridLayout, QLineEdit, QLabel, QSizePolicy, QSpacerItem, QWidget
from PyQt5.QtGui import QColor
import time


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(500)
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 4, 0, 0)
        self.label = QLabel("yo test")
        self.setProperty("loginForm", True)
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(100)
        boxShadow.setOffset(-50, 10)
        boxShadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(boxShadow)
        grid.addWidget(self.label)


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setProperty("loginPage", True)
        self.widget = QWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        grid = QGridLayout(self.widget)
        grid.setContentsMargins(0, 0, 0, 0)
        self.form = LoginForm()

        spacer_left = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addItem(spacer_left, 0, 0)
        grid.addWidget(self.form, 0, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.isHidden():
            if self.width() > 1200:
                self.form.setFixedWidth(int(self.width()/2) - 100)
            else:
                self.form.setFixedWidth(500)