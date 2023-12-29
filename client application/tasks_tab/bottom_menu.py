from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QApplication, QMainWindow, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QScrollArea, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap, QFont
from color_icon import color_pixmap
from PyQt5.QtCore import Qt, QSize, QDate
from qfluentwidgets import IconWidget, FluentIcon, InfoBarIcon, ProgressBar, AvatarWidget, CalendarPicker, ToolButton, InfoBar, InfoBarPosition, MenuAnimationType, RoundMenu, Action
import json


class User(QWidget):
    def __init__(self, user):
        super().__init__()
        # self.avatar = AvatarWidget()
        # self.avatar.setImage(user.profile_picture)
        # self.avatar.setRadius(12)
        # User avatar causes major lag to the application.
        self.icon = IconWidget(QIcon(user.profile_picture))
        self.icon.setFixedHeight(24)
        self.icon.setFixedWidth(24)
        self.username = QLabel(user.username)
        self.username.setStyleSheet("font-family:verdana;margin:0px;font-size:12px")
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 0, 0)
        # layout.addWidget(self.avatar)
        layout.addWidget(self.icon)
        layout.addWidget(self.username)


class Status(QWidget):
    def __init__(self, status):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.status_card = QLabel()
        self.layout.addWidget(self.status_card)
        if status == 0:
            self.status_card.setText("Upcoming")
            self.status_card.setProperty("status0", True)
        elif status == 1:
            self.status_card.setText("Active")
            self.status_card.setProperty("status1", True)
        elif status == 2:
            self.status_card.setText("Complete")
            self.status_card.setProperty("status2", True)
        else:
            self.status_card.setText("Expired")
            self.status_card.setProperty("status3", True)

    def setStatus(self, status):
        self.status_card.deleteLater()
        self.status_card = QLabel()
        self.layout.addWidget(self.status_card)
        if status == 0:
            self.status_card.setText("Upcoming")
            self.status_card.setProperty("status0", True)
        elif status == 1:
            self.status_card.setText("Active")
            self.status_card.setProperty("status1", True)
        elif status == 2:
            self.status_card.setText("Complete")
            self.status_card.setProperty("status2", True)
        else:
            self.status_card.setText("Expired")
            self.status_card.setProperty("status3", True)
        self.layout.addWidget(self.status_card)


class TimeLeft(QWidget):
    def __init__(self, timeleft_item):
        super().__init__()
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(10, 0, 0, 0)
        self.grid.setSpacing(0)
        self.label = QLabel(timeleft_item[0])
        self.label.setAlignment(Qt.AlignLeft)
        self.setProperty("TimeLeft", True)
        if timeleft_item[1] == 0:
            self.label.setProperty("TimeLeft0", True)
            self.icon = IconWidget(InfoBarIcon.SUCCESS)
        elif timeleft_item[1] == 1:
            self.label.setProperty("TimeLeft1", True)
            self.icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 2:
            self.label.setProperty("TimeLeft2", True)
            self.icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 3:
            self.label.setProperty("TimeLeft3", True)
            self.icon = IconWidget(InfoBarIcon.ERROR)
        else:
            self.label.setProperty("TimeLeft4", True)
            self.icon = IconWidget(FluentIcon.DATE_TIME)
        self.icon.setFixedHeight(20)
        self.icon.setFixedWidth(20)
        self.grid.addWidget(self.icon, 0, 0)
        self.grid.addWidget(self.label, 0, 1)

    def setTime(self, timeleft_item):
        self.label.deleteLater()
        self.icon.deleteLater()
        self.label = QLabel(timeleft_item[0])
        self.label.setAlignment(Qt.AlignLeft)
        self.setProperty("TimeLeft", True)
        if timeleft_item[1] == 0:
            self.label.setProperty("TimeLeft0", True)
            self.icon = IconWidget(InfoBarIcon.SUCCESS)
        elif timeleft_item[1] == 1:
            self.label.setProperty("TimeLeft1", True)
            self.icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 2:
            self.label.setProperty("TimeLeft2", True)
            self.icon = IconWidget(InfoBarIcon.WARNING)
        elif timeleft_item[1] == 3:
            self.label.setProperty("TimeLeft3", True)
            self.icon = IconWidget(InfoBarIcon.ERROR)
        else:
            self.label.setProperty("TimeLeft4", True)
            self.icon = IconWidget(FluentIcon.DATE_TIME)
        self.icon.setFixedHeight(20)
        self.icon.setFixedWidth(20)
        self.grid.addWidget(self.icon, 0, 0)
        self.grid.addWidget(self.label, 0, 1)


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
        self.file = None
        self.setContentsMargins(0, 0, 20, 21)
        self.setProperty("tasksTopMenu", True)
        self.parent = parent
        self.mainWindow = mainWindow
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)

        layout = QGridLayout(self.widget)

        self.filter = 0

        self.searchBar = QWidget()
        self.searchBar.setProperty("searchBar", True)
        self.searchBar.setFixedHeight(40)
        self.searchBar.setToolTip("Search tasks")
        self.searchBarQlineEdit = searchBarQLineEdit(self, self.mainWindow)
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
        self.task_list = []
        searchBarLayout.addWidget(self.searchBarQlineEdit, 0, 1)
        searchBarLayout.addWidget(self.searchBarIcon, 0, 0)

        self.tasksTableWidget = QTableWidget(0, 6)
        self.tasksTableWidget.setFocusPolicy(Qt.NoFocus)
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
        self.tasksTableWidget.contextMenuEvent = self.contextMenuEvent_table
        self.tasksTableWidget.cellDoubleClicked.connect(self.doubleClick)
        for col in range(3, self.tasksTableWidget.columnCount()):
            self.tasksTableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        layout.addWidget(self.searchBar, 0, 0)
        self.tasksDatePicker = CalendarPicker()
        self.tasksDatePicker.dateChanged.connect(self.date_tasks_filter)
        self.exportTasksButton = ToolButton()
        self.exportTasksButton.setIcon(FluentIcon.DOWNLOAD)
        self.exportTasksButton.setToolTip("Export tasks")
        self.exportTasksButton.mousePressEvent = self.exportMenu
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
            self.tasksTableWidget.setCellWidget(self.tasksTableWidget.rowCount() - 1, 5, progressBar(0))
            self.tasksTableWidget.setRowHeight(self.tasksTableWidget.rowCount() - 1, 40)
        self.parent.topMenu.setTaskNumber(len(task_list))

    def date_tasks_filter(self, date):
        self.parent.topMenu.setTab(None)
        self.searchBarQlineEdit.setDisabled(True)
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
        self.searchBarQlineEdit.setDisabled(False)
        if self.tasksDatePicker.property("hasDate"):
            self.tasksDatePicker.setText(self.tasksDatePicker.tr('Pick a date'))
            self.tasksDatePicker.setProperty('hasDate', False)
            self.tasksDatePicker.setStyle(QApplication.style())
            for row in range(self.tasksTableWidget.rowCount()):
                self.tasksTableWidget.showRow(row)

    def exportMenu(self, event):
        menu = RoundMenu(parent=self)
        visible_tasks = []
        selected_tasks = []
        menu.addActions([
            Action(FluentIcon.CLEAR_SELECTION, 'Export selected'),
            Action(FluentIcon.VIEW, 'Export visible'),
            Action(FluentIcon.GLOBE, 'Export all tasks')
        ])
        if len(self.tasksTableWidget.selectionModel().selectedRows()) == 0:
            menu.menuActions()[0].setDisabled(True)
        else:
            for row in self.tasksTableWidget.selectionModel().selectedRows():
                selected_tasks.append(self.task_list[row.row()])
        if len(self.task_list) == 0:
            menu.menuActions()[1].setDisabled(True)
            menu.menuActions()[2].setDisabled(True)
        else:
            menu.menuActions()[1].setDisabled(True)
            for row in range(self.tasksTableWidget.rowCount()):
                if not self.tasksTableWidget.isRowHidden(row):
                    menu.menuActions()[1].setDisabled(False)
                    visible_tasks.append(self.task_list[row])
        menu.menuActions()[0].triggered.connect(lambda: self.export(selected_tasks))
        menu.menuActions()[1].triggered.connect(lambda: self.export(visible_tasks))
        menu.menuActions()[2].triggered.connect(lambda: self.export(self.task_list))
        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

    def get_tasks(self, task_ids, f_type):
        message = json.dumps({"url": "/task_details", "method": "POST", "token": self.mainWindow.user.auth_token, "data": task_ids})
        if f_type == "CSV":
            self.mainWindow.init_send(message.encode(), self.tasks_to_csv)
        elif f_type == "PDF":
            self.mainWindow.init_send(message.encode(), self.tasks_to_pdf)

    def tasks_to_pdf(self, response):
        try:
            data = json.loads(response.decode())
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if data["status"] == 200:
            try:
                # ELMIRRRRR C'EST ICI C'EST ICI QUE TU VAS METTRE TA CLASSEEEEE
                # TaskPDF(data["data"], self.file)
                InfoBar.success(title="Export successful",content=f"Exported task(s) to {self.file}",parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)
            except Exception as err:
                print(err)
                InfoBar.error(title="Cancelled export",content="Something went wrong while creating PDF file",parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)
        elif data["status"] == 403:
            self.mainWindow.logout()
        else:
            InfoBar.error(title="Server error",content=data["message"],parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)

    def tasks_to_csv(self, response):
        try:
            data = json.loads(response.decode())
            print(data)
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if data["status"] == 200:
            try:
                content = "Task name,Tag\n"
                status = ["Upcoming", "Active", "Complete", "Expired"]
                for task in data["data"]:
                    content += f"{task['name']},{task['tag']}\n"
                with open(self.file, "w") as f:
                    f.write(content)
                f.close()
                InfoBar.success(title="Export successful",content=f"Exported task(s) to {self.file}",parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)
            except Exception as err:
                print(err)
                InfoBar.error(title="Cancelled export",content="Something went wrong while creating CSV file",parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)
        elif data["status"] == 403:
            self.mainWindow.logout()
        else:
            InfoBar.error(title="Server error",content=data["message"],parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)

    def export(self, tasks, task_id=None):
        try:
            file, _ = QFileDialog.getSaveFileName(self, "Choose File", "", "PDF Files (*.pdf);;CSV Files (*.csv)")
            if file is not None:
                # Determine the selected file extension
                if file.endswith(".pdf"):
                    InfoBar.info(title="Export", content=f"Exporting tasks to PDF...", parent=self.parent, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT,duration=5000)
                    file_format = "PDF"
                elif file.endswith(".csv"):
                    InfoBar.info(title="Export", content=f"Exporting tasks to CSV...", parent=self.parent, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT,duration=5000)
                    file_format = "CSV"
                else:
                    return InfoBar.error(title="Cancelled export", content="No file selected", parent=self.parent, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
                self.file = file
                task_ids = []
                if tasks is not None:
                    for task in tasks:
                        task_ids.append(task.id)
                else:
                    task_ids.append(task_id)
                self.get_tasks(task_ids, file_format)
        except Exception as err:
            InfoBar.error(title="Cancelled export",content="Something went wrong",parent=self.parent,orient=Qt.Horizontal,isClosable=True,position=InfoBarPosition.TOP_RIGHT,duration=5000)
            print(err)

    def __focus_search(self, event):
        self.searchBarQlineEdit.setFocus()

    def clearTasks(self):
        self.tasksTableWidget.clearContents()
        self.tasksTableWidget.setRowCount(0)

    def searchFilter(self, text):
        self.reset_date()
        if text != "":
            for row in range(self.tasksTableWidget.rowCount()):
                if text.lower() in self.tasksTableWidget.item(row, 0).text().lower() or text.lower() in self.tasksTableWidget.item(row, 1).text().lower():
                    self.tasksTableWidget.showRow(row)
                else:
                    self.tasksTableWidget.hideRow(row)
        else:
            for row in range(self.tasksTableWidget.rowCount()):
                self.tasksTableWidget.showRow(row)
        self.apply_filter()

    def apply_filter(self):
        if self.filter == 1:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].is_owner:
                    self.tasksTableWidget.hideRow(i)
        elif self.filter == 2:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].status == 1:
                    self.tasksTableWidget.hideRow(i)
        elif self.filter == 3:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].is_completed:
                    self.tasksTableWidget.hideRow(i)

    def create_task(self):
        self.mainWindow.create_task_form()

    def set_filter(self, x: int):
        self.reset_date()
        self.filter = x
        if self.filter == 0:
            for i in range(0, len(self.task_list)):
                self.tasksTableWidget.showRow(i)
        elif self.filter == 1:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].is_owner:
                    self.tasksTableWidget.hideRow(i)
                else:
                    self.tasksTableWidget.showRow(i)
        elif self.filter == 2:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].status == 1:
                    self.tasksTableWidget.hideRow(i)
                else:
                    self.tasksTableWidget.showRow(i)
        elif self.filter == 3:
            for i in range(0, len(self.task_list)):
                if not self.task_list[i].is_completed:
                    self.tasksTableWidget.hideRow(i)
                else:
                    self.tasksTableWidget.showRow(i)
        searchbartext = self.searchBarQlineEdit.text()
        if searchbartext != "":
            for row in range(self.tasksTableWidget.rowCount()):
                if searchbartext.lower() in self.tasksTableWidget.item(row, 0).text().lower() or searchbartext.lower() in self.tasksTableWidget.item(row, 1).text().lower():
                    pass
                else:
                    self.tasksTableWidget.hideRow(row)

    def update_tasks(self, change):
        if change:
            self.task_list = self.mainWindow.tasks
            self.apply_filter()
        for row in range(self.tasksTableWidget.rowCount()):
            self.tasksTableWidget.cellWidget(row, 4).setTime(self.task_list[row].time_left())
            if change:
                self.tasksTableWidget.cellWidget(row, 3).setStatus(self.task_list[row].status)

    def doubleClick(self, e):
        return self.mainWindow.init_view_task_window(self.task_list[e].id)

    def contextMenuEvent_table(self, e):
        menu = RoundMenu(parent=self)
        selected_tasks = []
        for row in self.tasksTableWidget.selectionModel().selectedRows():
            selected_tasks.append(self.task_list[row.row()])
        if len(selected_tasks) == 1:
            menu.addAction(Action(FluentIcon.MORE, 'View Task'))
            if selected_tasks[0].is_completed:
                menu.addAction(Action(FluentIcon.CLOSE, 'Set uncompleted'))
                menu.menuActions()[1].triggered.connect(lambda: self.mainWindow.set_task_completed(selected_tasks[0].id, False))
            else:
                menu.addAction(Action(FluentIcon.COMPLETED, 'Set completed'))
                menu.menuActions()[1].triggered.connect(lambda: self.mainWindow.set_task_completed(selected_tasks[0].id, True))
            menu.addAction(Action(FluentIcon.EDIT, 'Edit Task'))
            menu.addAction(Action(FluentIcon.SAVE_AS, 'Export Task'))
            menu.addAction(Action(FluentIcon.DELETE, 'Delete Task'))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.ADD, 'Create Task'))
            menu.menuActions()[0].triggered.connect(lambda: self.mainWindow.init_view_task_window(selected_tasks[0].id)) # View task
            menu.menuActions()[2].triggered.connect(lambda: self.mainWindow.init_edit_task_window(selected_tasks[0].id)) # EDIT TASK
            menu.menuActions()[3].triggered.connect(lambda: self.export(selected_tasks)) # Export tasks
            menu.menuActions()[4].triggered.connect(lambda: self.mainWindow.delete_task(selected_tasks[0].id))  # DELETE SINGLE TASK
            menu.menuActions()[5].triggered.connect(lambda: self.create_task()) # Create task
        elif len(selected_tasks) > 1:
            menu.addAction(Action(FluentIcon.SAVE_AS, 'Export Tasks'))
            menu.addAction(Action(FluentIcon.DELETE, 'Delete Tasks'))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.ADD, 'Create Task'))
            task_ids = []
            for i in selected_tasks:
                task_ids.append(i.id)
            menu.menuActions()[0].triggered.connect(lambda: self.export(selected_tasks))  # Export tasks
            menu.menuActions()[1].triggered.connect(lambda: self.mainWindow.delete_tasks(task_ids))  # DELETE MULTIPLE TASK
            menu.menuActions()[2].triggered.connect(lambda: self.create_task())  # Create task
        else:
            menu.addAction(Action(FluentIcon.ADD, 'Create Task'))
            menu.menuActions()[0].triggered.connect(lambda: self.create_task())  # Create task
        menu.exec(e.globalPos(), aniType=MenuAnimationType.NONE)
