from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout


class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel()
        self.title.setText("Tasks")
        self.title.setProperty("title", True)
        grid = QGridLayout(self)
        grid.addWidget(self.title, 0, 0)

    def setTitle(self, title: str):
        self.title.setText(title)
