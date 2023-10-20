from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QScrollArea
from PyQt5.QtGui import QCursor, QIcon, QColor
from color_icon import color_icon
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
        layout.setRowStretch(3, 2)
        self.buttons = []

        self.__add_button(text='  Tasks', toolTip="View tasks", icon_path='icons/58477.png', index=0, custom_property="firstButton")
        self.__add_button(text='  Activity', toolTip="View recent activity", icon_path='icons/activity.png', index=1)
        self.__add_button(text='  Calendar', toolTip="View task calendar", icon_path='icons/calendrier.png', index=2)
        self.__add_button(text='  Friends', toolTip="View friends list", icon_path='icons/gens.png', index=3)
        self.__add_button(text='  Settings', toolTip="Edit settings", icon_path='icons/126472.png', index=4, custom_property="lastButton")

        for button in self.buttons:
            layout.addWidget(button, self.buttons.index(button), 0, alignment=Qt.Qt.AlignTop)

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
                    i.setIcon(color_icon(i.iconPath, QColor(255, 255, 255)))
                else:
                    i.setIcon(QIcon(i.iconPath))
        self.__tabWidget.setCurrentIndex(index)
        self.buttons[index].setProperty("selected", True)
        self.buttons[index].setStyleSheet("")
        self.parent.titlebar.setTitle(self.buttons[index].text())
        if not self.parent.is_dark:
            self.buttons[index].setIcon(color_icon(self.buttons[index].iconPath, QColor(184, 4, 253)))
        else:
            self.buttons[index].setIcon(color_icon(self.buttons[index].iconPath, QColor(145, 110, 236)))

    def darkModeIcons(self):
        for i in self.buttons:
            if not i.property("selected"):
                i.setIcon(color_icon(i.iconPath, QColor(255, 255, 255)))
            else:
                i.setIcon(color_icon(i.iconPath, QColor(145, 110, 236)))

    def lightModeIcons(self):
        for i in self.buttons:
            if not i.property("selected"):
                i.setIcon(QIcon(i.iconPath))
            else:
                i.setIcon(color_icon(i.iconPath, QColor(184, 4, 253)))

    def __add_button(self, text, toolTip, icon_path, index, custom_property=None):
        iconSize = QSize()
        iconSize.setWidth(22)
        iconSize.setHeight(22)
        button = QToolButton()
        button.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        button.iconPath = icon_path
        button.setIconSize(iconSize)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setToolTip(toolTip)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.setFixedWidth(128)
        button.setFixedHeight(60)
        button.setText(text)
        button.clicked.connect(lambda: self.setTab(index))
        button.setProperty("selected", False)
        if custom_property is not None:
            button.setProperty(custom_property, True)
            button.setFixedHeight(90)
        self.buttons.append(button)
