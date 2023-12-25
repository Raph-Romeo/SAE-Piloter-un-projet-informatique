from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton
from tasks_tab.tasks_tab import TasksTab
from calendar_tab.calendar_tab import CalendarTab
from settings_tab import SettingsTab

# Test
class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)


class MainTabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.tasksTab = TasksTab(parent)
        self.calendarTab = CalendarTab(parent)
        self.addTab(self.tasksTab, "Tasks")

        self.addTab(Tab(), "Activity")
        self.addTab(self.calendarTab, "Calendar")
        self.addTab(Tab(), "Friends")
        self.addTab(SettingsTab(parent), "Settings")
        self.tabBar().hide()
