from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton
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

