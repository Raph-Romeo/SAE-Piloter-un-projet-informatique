from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QToolButton, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap, QPainter
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QSize


class MainNavbar(QScrollArea):

    def __init__(self, mainTabWidget, parent, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.__tabWidget = mainTabWidget
        self.parent = parent
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.Qt.AlignLeft)
        layout.setRowStretch(4, 2)
        iconSize = QSize()
        iconSize.setWidth(22)
        iconSize.setHeight(22)
        self.buttons = []

        self.tasksButton = QToolButton()
        self.tasksButton.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        self.tasksButton.iconPath = 'icons/58477.png'
        self.tasksButton.setIconSize(iconSize)
        self.tasksButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.tasksButton.setToolTip('View all tasks')
        self.tasksButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tasksButton.setFixedWidth(128)
        self.tasksButton.setFixedHeight(90)
        self.tasksButton.setText('  Tasks')
        self.tasksButton.clicked.connect(lambda: self.setTab(0))
        self.tasksButton.setProperty("firstButton", True)
        self.tasksButton.setProperty("selected", False)
        self.buttons.append(self.tasksButton)

        self.activityButton = QToolButton()
        self.activityButton.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        self.activityButton.iconPath = 'icons/activity.png'
        self.activityButton.setIconSize(iconSize)
        self.activityButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.activityButton.setToolTip('View recent activity')
        self.activityButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.activityButton.setFixedWidth(128)
        self.activityButton.setFixedHeight(60)
        self.activityButton.setText('  Activity')
        self.activityButton.clicked.connect(lambda: self.setTab(1))
        self.activityButton.setProperty("selected", False)
        self.buttons.append(self.activityButton)

        self.calendarButton = QToolButton()
        self.calendarButton.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        self.calendarButton.iconPath = 'icons/calendrier.png'
        self.calendarButton.setIconSize(iconSize)
        self.calendarButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.calendarButton.setToolTip('View task calendar')
        self.calendarButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calendarButton.setFixedWidth(128)
        self.calendarButton.setFixedHeight(60)
        self.calendarButton.setText('  Calendar')
        self.calendarButton.clicked.connect(lambda: self.setTab(2))
        self.calendarButton.setProperty("selected", False)
        self.buttons.append(self.calendarButton)

        self.friendsButton = QToolButton()
        self.friendsButton.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        self.friendsButton.iconPath = 'icons/gens.png'
        self.friendsButton.setIconSize(iconSize)
        self.friendsButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.friendsButton.setToolTip('View friend list')
        self.friendsButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.friendsButton.setFixedWidth(128)
        self.friendsButton.setFixedHeight(60)
        self.friendsButton.setText('  Friends')
        self.friendsButton.clicked.connect(lambda: self.setTab(3))
        self.friendsButton.setProperty("selected", False)
        self.buttons.append(self.friendsButton)

        self.settingsButton = QToolButton()
        self.settingsButton.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        self.settingsButton.iconPath = 'icons/126472.png'
        self.settingsButton.setIconSize(iconSize)
        self.settingsButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.settingsButton.setToolTip('Edit settings')
        self.settingsButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.settingsButton.setFixedWidth(128)
        self.settingsButton.setFixedHeight(90)
        self.settingsButton.setText('  Settings')
        self.settingsButton.clicked.connect(lambda: self.setTab(4))
        self.settingsButton.setProperty("lastButton", True)
        self.settingsButton.setProperty("selected", False)
        self.buttons.append(self.settingsButton)

        layout.addWidget(self.tasksButton, 1, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.activityButton, 2, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.calendarButton, 3, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.friendsButton, 4, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.settingsButton, 5, 0, alignment=Qt.Qt.AlignTop)

        self.setTab(0, True)

        if self.parent.is_dark:
            self.darkModeIcons()
        else:
            self.lightModeIcons()

    def setTab(self, index, force=False):
        if self.__tabWidget.currentIndex() is index and not force:
            return
        for i in self.buttons:
            if i.property("selected"):
                i.setProperty("selected", False)
                i.setStyleSheet("")
                if self.parent.is_dark:
                    color = QColor(255, 255, 255)
                    pixmap = QPixmap(i.iconPath)
                    painter = QPainter(pixmap)
                    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                    painter.fillRect(pixmap.rect(), color)
                    painter.end()
                    icon = QIcon(pixmap)
                    i.setIcon(icon)
                else:
                    i.setIcon(QIcon(i.iconPath))
        self.__tabWidget.setCurrentIndex(index)
        self.buttons[index].setProperty("selected", True)
        self.buttons[index].setStyleSheet("")
        if not self.parent.is_dark:
            color = QColor(184, 4, 253)
            pixmap = QPixmap(self.buttons[index].iconPath)
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), color)
            painter.end()
            icon = QIcon(pixmap)
            self.buttons[index].setIcon(icon)
        else:
            color = QColor(145, 110, 236)
            pixmap = QPixmap(self.buttons[index].iconPath)
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), color)
            painter.end()
            icon = QIcon(pixmap)
            self.buttons[index].setIcon(icon)

    def darkModeIcons(self):
        for i in self.buttons:
            if not i.property("selected"):
                color = QColor(255, 255, 255)
                pixmap = QPixmap(i.iconPath)
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter.fillRect(pixmap.rect(), color)
                painter.end()
                icon = QIcon(pixmap)
                i.setIcon(icon)
            else:
                color = QColor(145, 110, 236)
                pixmap = QPixmap(i.iconPath)
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter.fillRect(pixmap.rect(), color)
                painter.end()
                icon = QIcon(pixmap)
                i.setIcon(icon)

    def lightModeIcons(self):
        for i in self.buttons:
            if not i.property("selected"):
                i.setIcon(QIcon(i.iconPath))
            else:
                color = QColor(184, 4, 253)
                pixmap = QPixmap(i.iconPath)
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter.fillRect(pixmap.rect(), color)
                painter.end()
                icon = QIcon(pixmap)
                i.setIcon(icon)
