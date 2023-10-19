from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QToolButton, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor, QIcon
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QSize


class MainNavbar(QMainWindow):

    def __init__(self, mainTabWidget, parent):
        super().__init__()
        content = QWidget(self)
        self.setCentralWidget(content)
        self.__tabWidget = mainTabWidget
        self.parent = parent
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setStyleSheet("background:red")