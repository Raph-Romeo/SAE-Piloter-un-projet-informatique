from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QPushButton

class SettingsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout(self)
        self.button = QPushButton()
        self.parent = parent
        if self.parent.is_dark:
            self.button.setText("Light mode")
        else:
            self.button.setText("Dark mode")
        self.button.clicked.connect(self.toggleDarkmode)
        self.grid.addWidget(self.button)

    def toggleDarkmode(self):
        self.parent.toggleDarkmode()
        if self.parent.is_dark:
            self.button.setText("Light mode")
        else:
            self.button.setText("Dark mode")