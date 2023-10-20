from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)