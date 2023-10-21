from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton

class SettingsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()
        self.parent = parent
        if self.parent.is_dark:
            self.button.setText("Set theme to Light mode")
        else:
            self.button.setText("Set theme to Dark mode")
        self.button.clicked.connect(self.toggleDarkmode)
        self.button.setProperty("settings", True)
        self.grid.addWidget(self.button)

    def toggleDarkmode(self):
        self.parent.toggleDarkmode()
        if self.parent.is_dark:
            self.button.setText("Set theme to Light mode")
        else:
            self.button.setText("Set theme to Dark mode")