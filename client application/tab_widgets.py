from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton
from settings_tab import SettingsTab

# Test
class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)


class MainTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.addTab(Tab(), "Tasks")
        self.addTab(Tab(), "Activity")
        self.addTab(Tab(), "Calendar")
        self.addTab(Tab(), "Friends")
        self.addTab(SettingsTab(), "Settings")
        self.tabBar().hide()