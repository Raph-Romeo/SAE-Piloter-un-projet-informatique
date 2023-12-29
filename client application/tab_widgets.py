from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation
from tasks_tab.tasks_tab import TasksTab
from calendar_tab.calendar_tab import CalendarTab
from settings_tab.settings_tab import SettingsTab
from friends_tab.friends_tab import FriendsTab
from activity_tab.activity_tab import ActivityTab

class MainTabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.tasksTab = TasksTab(parent)
        self.calendarTab = CalendarTab(parent)
        self.settingsTab = SettingsTab(parent)
        self.friendsTab = FriendsTab(parent)
        self.activityTab = ActivityTab(parent)
        self.addTab(self.tasksTab, "Tasks")
        self.addTab(self.activityTab, "Activity")
        self.addTab(self.calendarTab, "Calendar")
        self.addTab(self.friendsTab, "Friends")
        self.addTab(self.settingsTab, "Settings")
        self.tabBar().hide()

        self.currentChanged.connect(self.handleTabChanged)

    def handleTabChanged(self, index):
        if index == 0:
            top_menu = self.tasksTab.topMenu
            if top_menu.widget.width() >= 560:
                top_menu.innerLeft.setFixedWidth(top_menu.leftWrapper.width() - 15)
                if not top_menu.leftWrapper.horizontalScrollBar().isHidden():
                    top_menu.leftWrapper.horizontalScrollBar().hide()
                    top_menu.leftWrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                top_menu.innerLeft.setFixedWidth(480)
                if top_menu.leftWrapper.horizontalScrollBar().isHidden():
                    top_menu.leftWrapper.horizontalScrollBar().show()
                    top_menu.leftWrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        elif index == 4:
            top_menu = self.settingsTab.topMenu
            top_menu.innerLeft.setFixedWidth(top_menu.leftWrapper.width())