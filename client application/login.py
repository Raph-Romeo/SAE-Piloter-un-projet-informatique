from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QGridLayout, QLineEdit, QLabel, QSizePolicy, QSpacerItem, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPropertyAnimation
from qfluentwidgets import InfoBar, InfoBarPosition
import time


class LoginForm(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setFixedWidth(500)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        grid = QGridLayout(self.widget)
        grid.setContentsMargins(40, 32, 40, 0)
        self.setProperty("loginForm", True)
        self.parent = parent
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(200)
        boxShadow.setOffset(-20, 90)
        boxShadow.setColor(QColor(0, 0, 0, 180))

        self.usernameInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        self.usernameInput.setProperty("loginButton", True)
        self.passwordInput.setProperty("loginButton", True)
        self.passwordInput.setMaximumWidth(450)
        self.usernameInput.setMaximumWidth(450)

        self.usernameInput.returnPressed.connect(self.login)
        self.passwordInput.returnPressed.connect(self.login)

        self.setGraphicsEffect(boxShadow)
        grid.addWidget(self.usernameInput)
        grid.addWidget(self.passwordInput)
        grid.setAlignment(Qt.AlignCenter)


    def login(self):
        if len(self.usernameInput.text()) == 0 or len(self.passwordInput.text()) == 0:
            pass
        else:
            if self.usernameInput.text() == "toto" and self.passwordInput.text() == "toto":
                self.usernameInput.setDisabled(True)
                self.passwordInput.setDisabled(True)
                self.hide()
                self.parent.fade(self.parent)
            else:
                InfoBar.error(
                    title="Failed to login",
                    content="Incorrect credentials",
                    parent = self.parent,
                    orient=Qt.Horizontal,
                    isClosable= True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration = 2000
                )


class Login(QMainWindow):
    def __init__(self, darkmode: bool):
        super().__init__()
        self.setProperty("loginPage", True)
        self.widget = QWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        grid = QGridLayout(self.widget)
        grid.setContentsMargins(0, 0, 0, 0)
        self.form = LoginForm(self)
        if darkmode:
            self.backgroundPath = "background/dark_login.jpg"
        else:
            self.backgroundPath = "background/light_login.jpg"
        self.setStyleSheet('QMainWindow[loginPage="true"]{border-image:url(' + self.backgroundPath + ')}')
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

    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        self.form.hide()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self.animation.finished.connect(self.hide)

    def show(self):
        super().show()
        self.form.show()

    def hide(self):
        super().hide()
        self.setStyleSheet('QMainWindow[loginPage="true"]{border-image:none}')
