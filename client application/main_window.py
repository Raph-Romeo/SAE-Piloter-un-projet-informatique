from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QColor
from stylesheets import dark_style_sheet, light_style_sheet
from navbar import MainNavbar
from tab_widgets import MainTabWidget
from titlebar import TitleBar
from qframelesswindow import FramelessWindow, StandardTitleBar
from login import Login
from qfluentwidgets import setTheme, Theme
from datetime import datetime
from PyQt5.QtGui import QImage
import requests


class Task:
    def __init__(self, name, tag, date_created, start_date, deadline, owner, user, public=False):
        self.name = name
        self.tag = tag
        self.date_created = date_created
        self.start_date = start_date
        self.deadline = deadline
        self.owner = owner
        self.user = user
        self.public = public


class User:
    def __init__(self, username, email, profile_picture_url=None, token=None):
        self.username = username
        image = "icons/default.png"
        if profile_picture_url is not None:
            try:
                image = QImage()
                image.loadFromData(requests.get(profile_picture_url).content)
            except:
                pass
        self.profile_picture = image
        self.auth_token = token
        self.email = email


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.stb = StandardTitleBar(self)
        self.stb.setTitle("Taskmaster PRO")
        self.stb.setIcon(QIcon('icons/taskmasterpro.png'))
        self.stb.iconLabel.setStyleSheet("margin:0;padding:0")
        self.setTitleBar(self.stb)
        self.setProperty("MainWindow", True)
        self.resize(820, 534)
        self.setMinimumSize(520, 274)
        self.is_dark = False
        self.mainTabWidget = MainTabWidget(self)
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)
        self.titlebar = TitleBar(self)
        self.titlebar.setFixedHeight(74)
        self.titlebar.setContentsMargins(0, 28, 0, 0)
        self.navbar = MainNavbar(self.mainTabWidget, self)
        self.navbar.setFixedWidth(148)
        if self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()
        grid.addWidget(self.titlebar, 0, 1)
        grid.addWidget(self.navbar, 0, 0, 2, 1)
        grid.addWidget(self.mainTabWidget, 1, 1, 1, 1)

        self.login_page = Login(self)
        grid.addWidget(self.login_page, 0, 0, 2, 2)

        self.titleBar.raise_()

    def toggleDarkmode(self):
        if not self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()

    def setDarkMode(self):
        self.setStyleSheet(dark_style_sheet)
        self.is_dark = True
        self.navbar.darkModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.DARK)

    def setLightMode(self):
        self.setStyleSheet(light_style_sheet)
        self.is_dark = False
        self.navbar.lightModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.LIGHT)

    def connectGetTasksAndEverything(self):
        self.user = User("toto", "toto@toto.com", profile_picture_url="https://img6.arthub.ai/63d88fba-d272.webp")
        self.tasks = [
            Task("task A", "Home", datetime(2003, 5, 14), datetime(2023, 10, 25, hour=3), datetime(2023, 10, 25, hour=4), self.user,self.user),
            Task("task B", "Home", datetime(2003, 5, 14), datetime(2023, 10, 25, hour=6), datetime(2023, 10, 25, hour=4), self.user,self.user),
            Task("task C", "Home", datetime(2003, 5, 14), datetime(2023, 10, 25, hour=6), datetime(2023, 10, 25, hour=4), self.user, self.user),

        ]
        self.mainTabWidget.tasksTab.update_tasks(self.tasks)
        self.mainTabWidget.calendarTab.initiate_calendar()
        self.titlebar.setUserPanel(self.user)

    def logout(self):
        self.user = None
        self.login_page.fadeIn()
