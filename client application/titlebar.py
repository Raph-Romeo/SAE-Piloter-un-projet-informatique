from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import MenuAnimationType, RoundMenu, FluentIcon, Action, AvatarWidget, BodyLabel, CaptionLabel, isDarkTheme
from PyQt5.QtGui import QColor, QCursor


class ProfileCard(QWidget):

    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.emailLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        self.setFixedSize(260, 64)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)


class TitleBar(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.title = QLabel()
        self.title.setText("Tasks")
        self.title.setProperty("title", True)
        grid = QGridLayout(self)
        grid.setContentsMargins(5, 5, 35, 5)
        grid.addWidget(self.title, 0, 0)
        self.setFixedHeight(60)
        self.mainwindow = mainwindow
        self.user_panel = QWidget()
        self.user_panel.setProperty("userPanel", True)
        self.user_panel.setStyleSheet("QWidget[userPanel]:hover{border-radius:16px;background:rgba(120,120,120,0.1);}")
        self.user_grid = QGridLayout(self.user_panel)
        self.user_grid.setContentsMargins(0, 4, 5, 20)
        self.user_panel.setCursor(QCursor(Qt.PointingHandCursor))
        self.username = QLabel("...")
        self.username.setProperty("username_title", True)
        self.username.setMaximumWidth(120)
        self.username.setWordWrap(False)
        self.username.setFixedHeight(32)
        self.username.setAlignment(Qt.AlignVCenter)
        self.user_grid.addWidget(self.username, 0, 0)
        self.user_grid.setSpacing(8)
        self.user_panel.setFixedHeight(40)
        self.user_panel.mousePressEvent = self.userDetailsMenu
        grid.addWidget(self.user_panel, 0, 1, alignment=Qt.AlignRight)

    def setTitle(self, title: str):
        self.title.setText(title)

    def setUserPanel(self, user):
        self.user = user
        self.username.setText(self.user.username)
        avatarWidget = AvatarWidget(self.user.profile_picture, self)
        avatarWidget.setRadius(16)
        avatarWidget.setProperty("profile_picture_title", True)
        self.user_grid.addWidget(avatarWidget, 0, 1)

    def userDetailsMenu(self, e):
        menu = RoundMenu(parent=self)
        card = ProfileCard(self.user.profile_picture, self.user.username, self.user.email, menu)
        menu.addWidget(card, selectable=False)
        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.PEOPLE, 'Friends'),
            Action(FluentIcon.SETTING, 'Edit profile')
        ])
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.PAGE_LEFT, 'Sign-out'))
        menu.menuActions()[1].triggered.connect(lambda: self.mainwindow.navbar.setTab(3))
        menu.menuActions()[2].triggered.connect(self.edit_profile)
        menu.menuActions()[3].triggered.connect(lambda: self.mainwindow.logout())
        menu.exec(e.globalPos(), aniType=MenuAnimationType.NONE)

    def edit_profile(self):
        self.mainwindow.navbar.setTab(4)
        self.mainwindow.mainTabWidget.settingsTab.topMenu.setTab(1)
