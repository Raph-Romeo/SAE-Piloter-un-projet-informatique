from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QGridLayout, QVBoxLayout, QLineEdit, QLabel, QSizePolicy, QSpacerItem, QWidget
from PyQt5.QtGui import QColor, QCursor, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation
from qfluentwidgets import InfoBar, InfoBarPosition, FluentIcon, Theme, AvatarWidget
import json
import hashlib


class LoginForm(QMainWindow):
    def __init__(self, parent, init_send):
        super().__init__()
        self.setFixedWidth(500)
        self.init_send = init_send
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        grid = QGridLayout(self.widget)
        grid.setContentsMargins(40, 0, 40, 0)
        self.setProperty("loginForm", True)
        self.parent = parent
        self.currentForm = 0
        boxShadow = QGraphicsDropShadowEffect()
        boxShadow.setBlurRadius(200)
        boxShadow.setOffset(-20, 90)
        boxShadow.setColor(QColor(0, 0, 0, 180))

        # Login form

        self.loginForm = QWidget()
        loginFormLayout = QVBoxLayout(self.loginForm)
        loginFormLayout.setContentsMargins(0, 0, 0, 0)

        self.usernameInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username or Email")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        self.usernameInput.setProperty("loginButton", True)
        self.passwordInput.setProperty("loginButton", True)
        self.passwordInput.setMaximumWidth(450)
        self.usernameInput.setMaximumWidth(450)

        loginFormLayout.addWidget(self.usernameInput)
        loginFormLayout.addWidget(self.passwordInput)

        # Sign up form

        self.signUpFormPage = 0

        self.signUpForm = QWidget()
        self.signUpForm.hide()
        self.signUpFormLayout = QVBoxLayout(self.signUpForm)
        self.signUpFormLayout.setContentsMargins(0, 0, 0, 0)

        self.chooseUsernameInput = QLineEdit()
        self.chooseUsernameInput.setPlaceholderText("Username")
        self.chooseUsernameInput.setProperty("loginButton", True)
        self.chooseUsernameInput.setMaximumWidth(450)
        self.chooseUsernameInput.hide()

        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Email")
        self.emailInput.setProperty("loginButton", True)
        self.emailInput.setMaximumWidth(450)
        self.emailInput.hide()

        self.choosePasswordInput = QLineEdit()
        self.choosePasswordInput.setPlaceholderText("Password")
        self.choosePasswordInput.setEchoMode(QLineEdit.Password)
        self.choosePasswordInput.setProperty("loginButton", True)
        self.choosePasswordInput.setMaximumWidth(450)
        self.choosePasswordInput.hide()

        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setPlaceholderText("Confirm password")
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)
        self.confirmPasswordInput.setProperty("loginButton", True)
        self.confirmPasswordInput.setMaximumWidth(450)
        self.confirmPasswordInput.hide()

        self.profilePicture = AvatarWidget("icons/default.png", self)
        self.profilePicture.setRadius(32)
        self.profilePicture.setCursor(QCursor(Qt.PointingHandCursor))
        self.profilePicture.hide()
        self.profilePicture.setAlignment(Qt.AlignCenter)

        self.firstNameInput = QLineEdit()
        self.firstNameInput.setPlaceholderText("First Name")
        self.firstNameInput.setProperty("loginButton", True)
        self.firstNameInput.setMaximumWidth(450)
        self.firstNameInput.hide()

        self.lastNameInput = QLineEdit()
        self.lastNameInput.setPlaceholderText("Last Name")
        self.lastNameInput.setProperty("loginButton", True)
        self.lastNameInput.setMaximumWidth(450)
        self.lastNameInput.hide()

        self.pageControl = QWidget()
        layout = QHBoxLayout(self.pageControl)
        self.pageControl.setFixedWidth(60)

        self.nextPageButton = QPushButton()
        self.nextPageButton.setToolTip("Next page")
        self.nextPageButton.setFixedWidth(20)
        self.nextPageButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.nextPageButton.clicked.connect(lambda: self.setSignUpFormPage(self.signUpFormPage + 1))
        self.previousPageButton = QPushButton()
        self.previousPageButton.setToolTip("Previous page")
        self.previousPageButton.setDisabled(True)
        self.previousPageButton.setFixedWidth(20)
        self.previousPageButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.previousPageButton.clicked.connect(lambda: self.setSignUpFormPage(self.signUpFormPage - 1))

        layout.addWidget(self.previousPageButton)
        layout.addWidget(self.nextPageButton)

        self.signUpFormLayout.addWidget(self.chooseUsernameInput)
        self.signUpFormLayout.addWidget(self.emailInput)

        self.signUpFormLayout.addWidget(self.choosePasswordInput)
        self.signUpFormLayout.addWidget(self.confirmPasswordInput)

        self.signUpFormLayout.addWidget(self.profilePicture)
        self.signUpFormLayout.addWidget(self.firstNameInput)
        self.signUpFormLayout.addWidget(self.lastNameInput)

        self.signUpFormLayout.addWidget(self.pageControl)

        self.setSignUpFormPage(self.signUpFormPage)

        # _____________________________________

        self.signUpButton = QPushButton()
        self.signUpButton.setText("Create account")
        self.signUpButton.setProperty("signupFormButton", True)
        self.signUpButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpButton.setFocusPolicy(Qt.NoFocus)
        self.signUpButton.clicked.connect(self.toggleForm)

        self.formTitle = QLabel("Login")
        self.formTitle.setStyleSheet("color:rgba(255,255,255,0.5);font-size:26px;font-weight:bold;font-family:verdana;margin-bottom:50px;")

        self.usernameInput.returnPressed.connect(self.login)
        self.passwordInput.returnPressed.connect(self.login)

        self.setGraphicsEffect(boxShadow)
        grid.addWidget(self.formTitle)
        grid.addWidget(self.loginForm)
        grid.addWidget(self.signUpForm)
        grid.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.signUpButton)


    def login(self):
        if len(self.usernameInput.text()) == 0 or len(self.passwordInput.text()) == 0:
            if len(self.usernameInput.text()) == 0:
                InfoBar.warning(
                        title="Form is not valid",
                        content="Please insert a username",
                        parent=self.parent,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2000
                )
            else:
                InfoBar.warning(
                        title="Form is not valid",
                        content="Please insert a password",
                        parent=self.parent,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2000
                )
        else:
            self.usernameInput.setDisabled(True)
            self.passwordInput.setDisabled(True)
            message = {"url": "/auth", "method": "POST", "data": {"username": self.usernameInput.text(), "password": hashlib.md5(self.passwordInput.text().encode("utf-8"), usedforsecurity=True).hexdigest()}}
            data = json.dumps(message)
            self.init_send(data.encode(), self.login_response)

    def login_response(self, response: bytes):
        response = json.loads(response.decode())
        if response["status"] == 200:
            self.hide()
            self.parent.fade(self.parent)
            self.parent.mainwindow.loadSession(response["data"])
        elif response["status"] == 401:
            InfoBar.error(
                title="Failed to login",
                content=response["message"],
                parent=self.parent,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000
            )
        elif response["status"] == 400:
            InfoBar.error(
                title="Server error",
                content=response["message"],
                parent=self.parent,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000
            )
        self.usernameInput.setDisabled(False)
        self.passwordInput.setDisabled(False)

    def toggleForm(self):
        if self.currentForm == 0:
            self.currentForm = 1
            self.signUpForm.setHidden(False)
            self.loginForm.hide()
            self.signUpButton.setText("Cancel")
            self.formTitle.setText("Sign-up")
        else:
            self.currentForm = 0
            self.loginForm.setHidden(False)
            self.signUpForm.hide()
            self.signUpButton.setText("Create account")
            self.formTitle.setText("Login")

    def setSignUpFormPage(self, page: int):
        self.signUpFormPage = page
        if page == 0:
            self.chooseUsernameInput.setHidden(False)
            self.emailInput.setHidden(False)
            self.choosePasswordInput.setHidden(True)
            self.confirmPasswordInput.setHidden(True)
            self.profilePicture.setHidden(True)
            self.firstNameInput.setHidden(True)
            self.lastNameInput.setHidden(True)
            self.previousPageButton.setDisabled(True)
        elif page == 1:
            self.chooseUsernameInput.setHidden(True)
            self.emailInput.setHidden(True)
            self.choosePasswordInput.setHidden(False)
            self.confirmPasswordInput.setHidden(False)
            self.profilePicture.setHidden(True)
            self.firstNameInput.setHidden(True)
            self.lastNameInput.setHidden(True)
            self.previousPageButton.setDisabled(False)
        elif page == 2:
            self.chooseUsernameInput.setHidden(True)
            self.emailInput.setHidden(True)
            self.choosePasswordInput.setHidden(True)
            self.confirmPasswordInput.setHidden(True)
            self.profilePicture.setHidden(False)
            self.firstNameInput.setHidden(False)
            self.lastNameInput.setHidden(False)


class Login(QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()
        self.setProperty("loginPage", True)
        self.widget = QWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        grid = QGridLayout(self.widget)
        grid.setContentsMargins(0, 0, 0, 0)
        self.form = LoginForm(self, mainwindow.init_send)
        self.mainwindow = mainwindow
        if self.mainwindow.is_dark:
            self.backgroundPath = "background/dark_login.jpg"
            self.form.previousPageButton.setIcon(QIcon(FluentIcon.PAGE_LEFT.icon(theme=Theme.DARK)))
            self.form.nextPageButton.setIcon(QIcon(FluentIcon.PAGE_RIGHT.icon(theme=Theme.DARK)))
        else:
            self.backgroundPath = "background/light_login.jpg"
            self.form.previousPageButton.setIcon(QIcon(FluentIcon.PAGE_LEFT.icon()))
            self.form.nextPageButton.setIcon(QIcon(FluentIcon.PAGE_RIGHT.icon()))
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

    def fadeIn(self):
        self.setHidden(False)
        if self.mainwindow.is_dark:
            self.backgroundPath = "background/dark_login.jpg"
            self.form.previousPageButton.setIcon(QIcon(FluentIcon.PAGE_LEFT.icon(theme=Theme.DARK)))
            self.form.nextPageButton.setIcon(QIcon(FluentIcon.PAGE_RIGHT.icon(theme=Theme.DARK)))
        else:
            self.backgroundPath = "background/light_login.jpg"
            self.form.previousPageButton.setIcon(QIcon(FluentIcon.PAGE_LEFT.icon()))
            self.form.nextPageButton.setIcon(QIcon(FluentIcon.PAGE_RIGHT.icon()))
        self.setStyleSheet('QMainWindow[loginPage="true"]{border-image:url(' + self.backgroundPath + ')}')
        self.form.usernameInput.setDisabled(False)
        self.form.passwordInput.setDisabled(False)
        self.form.passwordInput.setText("")
        self.effect = QGraphicsOpacityEffect()
        self.form.setHidden(False)
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.animation.finished.connect(lambda: self.setGraphicsEffect(None))
        self.form.usernameInput.setStyleSheet("")
        self.form.passwordInput.setStyleSheet("")

    def hide(self):
        super().hide()
        self.setStyleSheet('QMainWindow[loginPage="true"]{border-image:none}')
