from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QApplication, QMainWindow, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QScrollArea, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap, QFont
from color_icon import color_pixmap
from PyQt5.QtCore import Qt, QSize, QDate
from qfluentwidgets import IconWidget, FluentIcon, InfoBarIcon, ProgressBar, AvatarWidget, CalendarPicker, ToolButton

class User(QWidget):
    def __init__(self, user):
        super().__init__()
        self.avatar = AvatarWidget()
        self.avatar.setImage(user.profile_picture)
        self.avatar.setRadius(12)
        self.username = QLabel(user.username)
        self.username.setStyleSheet("font-family:verdana;margin:0px;font-size:12px")
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.avatar)
        layout.addWidget(self.username)


class Status(QWidget):
    def __init__(self, status):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        status_card = QLabel()
        layout.addWidget(status_card)
        if status == 0:
            status_card.setText("Upcoming")
            status_card.setProperty("status0", True)
        elif status == 1:
            status_card.setText("Active")
            status_card.setProperty("status1", True)
        elif status == 2:
            status_card.setText("Complete")
            status_card.setProperty("status2", True)
        else:
            status_card.setText("Expired")
            status_card.setProperty("status3", True)


class TimeLeft(QWidget):
    def __init__(self, timeleft_item):
        super().__init__()
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        label = QLabel(timeleft_item[0])
        label.setAlignment(Qt.AlignLeft)
        self.setProperty("TimeLeft", True)
        if timeleft_item[1] == 0:
            label.setProperty("TimeLeft0", True)
            icon = IconWidget(InfoBarIcon.SUCCESS)
        elif timeleft_item[1] == 1:
            label.setProperty("TimeLeft1", True)
            icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 2:
            label.setProperty("TimeLeft2", True)
            icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 3:
            label.setProperty("TimeLeft3", True)
            icon = IconWidget(InfoBarIcon.ERROR)
        else:
            label.setProperty("TimeLeft4", True)
            icon = IconWidget(FluentIcon.DATE_TIME)
        icon.setFixedHeight(20)
        icon.setFixedWidth(20)
        self.grid.addWidget(icon, 0, 0)
        self.grid.addWidget(label, 0, 1)

class progressBar(QWidget):
    def __init__(self, percentage):
        super().__init__()
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(5, 0, 5, 0)
        self.grid.setSpacing(0)
        self.progress_bar = ProgressBar()
        self.progress_bar.setValue(percentage)
        self.grid.addWidget(self.progress_bar)


class searchBarQLineEdit(QLineEdit):
    def __init__(self, parent, mainWindow):
        super().__init__()
        self.parent = parent
        self.mainWindow = mainWindow
        self.textChanged.connect(lambda: self.parent.searchFilter(self.text()))

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.parent.searchBar.setProperty("focused", True)
        if self.mainWindow.is_dark:
            pixmap = color_pixmap("icons/149852.png", QColor(200, 200, 200))
        else:
            pixmap = color_pixmap("icons/149852.png", QColor(34, 34, 34))
        self.parent.searchBarIcon.setPixmap(pixmap.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.parent.searchBar.setStyleSheet("")

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.parent.searchBar.setProperty("focused", False)
        pixmap = color_pixmap("icons/149852.png", QColor(100, 100, 100))
        self.parent.searchBarIcon.setPixmap(pixmap.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.parent.searchBar.setStyleSheet("")


class BottomMenu(QMainWindow):
    def __init__(self, mainWindow, parent):
        super().__init__()
        self.setContentsMargins(0, 0, 20, 21)
        self.setProperty("tasksTopMenu", True)
        self.parent = parent
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)

        layout = QGridLayout(self.widget)

        self.searchBar = QWidget()
        self.searchBar.setProperty("searchBar", True)
        self.searchBar.setFixedHeight(40)
        self.searchBar.setToolTip("Search tasks")
        self.searchBarQlineEdit = searchBarQLineEdit(self, mainWindow)
        self.searchBarQlineEdit.setPlaceholderText("Search tasks")
        self.searchBar.mousePressEvent = self.__focus_search
        self.searchBarQlineEdit.setFixedHeight(40)
        searchBarLayout = QGridLayout()
        self.searchBarIcon = QLabel()
        pixmap = color_pixmap("icons/149852.png", QColor(100, 100, 100))
        self.searchBarIcon.setFixedHeight(28)
        self.searchBar.setCursor(QCursor(Qt.IBeamCursor))
        self.searchBarIcon.setPixmap(pixmap.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.searchBar.setLayout(searchBarLayout)
        searchBarLayout.addWidget(self.searchBarQlineEdit, 0, 1)
        searchBarLayout.addWidget(self.searchBarIcon, 0, 0)

        self.tasksTableWidget = QTableWidget(0, 6)
        self.tasksTableWidget.setHorizontalHeaderLabels(["Task name", "Tag", "User", "Status", "Time left", "Progress"])
        self.tasksTableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{border-bottom:none}")
        font = QFont()
        font.setFamily("verdana")
        font.setPointSize(10)
        self.tasksTableWidget.horizontalHeader().setFont(font)
        self.tasksTableWidget.setFont(font)
        self.tasksTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tasksTableWidget.verticalHeader().setVisible(False)
        self.tasksTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tasksTableWidget.setShowGrid(False)
        self.tasksTableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tasksTableWidget.horizontalHeader().setSectionsClickable(False)
        for col in range(1, self.tasksTableWidget.columnCount()):
            self.tasksTableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        layout.addWidget(self.searchBar, 0, 0)
        self.tasksDatePicker = CalendarPicker()
        self.tasksDatePicker.dateChanged.connect(self.date_tasks_filter)
        self.exportTasksButton = ToolButton()
        self.exportTasksButton.setIcon(FluentIcon.DOWNLOAD)
        self.exportTasksButton.setToolTip("Export tasks")
        self.exportTasksButton.clicked.connect(self.exportTasks)
        layout.addWidget(self.tasksDatePicker, 0, 1)
        layout.addWidget(self.exportTasksButton, 0, 2)
        layout.addWidget(self.tasksTableWidget, 1, 0, 1, 3)

    def set_tasks(self, task_list):
        self.clearTasks()
        self.task_list = task_list
        for i in task_list:
            self.tasksTableWidget.setRowCount(self.tasksTableWidget.rowCount() + 1)
            self.tasksTableWidget.setItem(self.tasksTableWidget.rowCount() - 1, 0, QTableWidgetItem(i.name))
            self.tasksTableWidget.setItem(self.tasksTableWidget.rowCount() - 1, 1, QTableWidgetItem(i.tag))
            self.tasksTableWidget.setCellWidget(self.tasksTableWidget.rowCount() - 1, 2, User(i.user))
            self.tasksTableWidget.setCellWidget(self.tasksTableWidget.rowCount() - 1, 3, Status(i.status))
            self.tasksTableWidget.setCellWidget(self.tasksTableWidget.rowCount() - 1, 4, TimeLeft(i.time_left()))
            self.tasksTableWidget.setCellWidget(self.tasksTableWidget.rowCount() - 1, 5, progressBar(25))
            self.tasksTableWidget.setRowHeight(self.tasksTableWidget.rowCount() - 1, 40)
        self.parent.topMenu.setTaskNumber(len(task_list))

    def date_tasks_filter(self, date):
        for task in self.task_list:
            if task.deadline != None:
                if task.start_date.date() <= date.toPyDate() <= task.deadline.date():
                    self.tasksTableWidget.showRow(self.task_list.index(task))
                else:
                    self.tasksTableWidget.hideRow(self.task_list.index(task))
            else:
                if task.start_date.date() == date.toPyDate():
                    self.tasksTableWidget.showRow(self.task_list.index(task))
                else:
                    self.tasksTableWidget.hideRow(self.task_list.index(task))

    def reset_date(self):
        if self.tasksDatePicker.property("hasDate"):
            self.tasksDatePicker.setText(self.tasksDatePicker.tr('Pick a date'))
            self.tasksDatePicker.setProperty('hasDate', False)
            self.tasksDatePicker.setStyle(QApplication.style())
            for row in range(self.tasksTableWidget.rowCount()):
                self.tasksTableWidget.showRow(row)

    def exportTasks(self):
        try:
            fileDialog = QFileDialog()
            fileDialog.show()
            content = ""
            for task in self.task_list:
                content += f"{task.name}\n"
        except:
            pass

    def __focus_search(self, event):
        self.searchBarQlineEdit.setFocus()

    def clearTasks(self):
        self.tasksTableWidget.clearContents()
        self.tasksTableWidget.setRowCount(0)

    def searchFilter(self, text):
        if text != "":
            for row in range(self.tasksTableWidget.rowCount()):
                if text.lower() in self.tasksTableWidget.item(row, 0).text().lower() or text.lower() in self.tasksTableWidget.item(row, 1).text().lower():
                    self.tasksTableWidget.showRow(row)
                else:
                    self.tasksTableWidget.hideRow(row)
        else:
            for row in range(self.tasksTableWidget.rowCount()):
                self.tasksTableWidget.showRow(row)
