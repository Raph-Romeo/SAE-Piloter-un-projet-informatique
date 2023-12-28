from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from stylesheets import dark_style_sheet, light_style_sheet
from navbar import MainNavbar
from tab_widgets import MainTabWidget
from titlebar import TitleBar
from qframelesswindow import FramelessWindow, StandardTitleBar
from login import Login
from qfluentwidgets import setTheme, Theme
from datetime import datetime, timedelta
from PyQt5.QtGui import QImage
from view_task import ViewTask
import threading
import time
import socket
import requests
import json
from create_task import CreateTaskForm


class SendMessageWorker(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(bytes)
    error = pyqtSignal()

    def __init__(self, connection, message: bytes):
        super().__init__()
        self.connection = connection
        self.msg = message

    def run(self):
        try:
            remote_ip, remote_port = self.connection.getpeername()
            conn = socket.socket()
            conn.connect((remote_ip, remote_port))
            conn.send(self.msg)
            response = conn.recv(4096)
            self.message.emit(response)
            conn.close()
        except:
            self.error.emit()
            response = json.dumps({"status": 0}).encode()
            self.message.emit(response)
        return self.finished.emit()


class ClockThread(QObject):
    finished = pyqtSignal()
    update = pyqtSignal()

    def run(self):
        while True:
            time.sleep(1)
            self.update.emit()


class Task:
    def __init__(self, pk_id: int, name: str, tag: str, start_date, deadline, user, is_owner: bool = False,
                 public: bool = False, is_completed: bool = False):
        self.id = pk_id
        self.name = name
        self.tag = tag
        self.start_date = start_date
        self.deadline = deadline
        self.user = user
        self.is_completed = is_completed
        self.public = public
        self.status = None
        self.is_owner = is_owner
        self.update_status()

    def update_status(self):
        # Status - 0 = Upcoming, 1 = Active, 2 = Complete, 3 = Expired
        status = self.status
        if self.is_completed:
            self.status = 2
        elif datetime.now() < self.start_date:
            self.status = 0
        elif self.deadline is not None and self.start_date < datetime.now() < self.deadline:
            self.status = 1
        elif self.deadline is not None:
            self.status = 3
        else:
            self.status = 1
        if status != self.status:
            return True
        else:
            return False

    def time_left(self):
        if self.status != 2 and self.deadline is not None and datetime.now() > self.start_date:
            if self.deadline is None:
                return ["No limit", 0]
            delta = self.deadline - datetime.now()
            timestamp_timeleft = delta.days * 86400 + delta.seconds
            if timestamp_timeleft > 0:
                if timestamp_timeleft > 86400:
                    return [f"{delta.days} day(s)", 1]
                elif timestamp_timeleft > 3600:
                    return [f"{int(delta.seconds / 3600)} hour(s)", 1]
                elif timestamp_timeleft > 60:
                    return [f"{int(delta.seconds / 60)} minute(s)", 1]
                else:
                    return [f"{int(delta.seconds)} second(s)", 2]
            else:
                return ["Expired", 3]
        else:
            if self.deadline is None:
                delta = self.start_date - datetime.now()
            else:
                delta = self.deadline - datetime.now()
            timestamp_timeleft = delta.days * 86400 + delta.seconds
            if timestamp_timeleft > 0:
                if timestamp_timeleft > 86400:
                    return [f"{delta.days} day(s)", 4]
                elif timestamp_timeleft > 3600:
                    return [f"{int(delta.seconds / 3600)} hour(s)", 4]
                elif timestamp_timeleft > 60:
                    return [f"{int(delta.seconds / 60)} minute(s)", 4]
                else:
                    return [f"{int(delta.seconds)} second(s)", 4]
            else:
                return [f"{str(self.start_date)}", 4]


class User:
    def __init__(self, username, email, profile_picture_url=None, token=None):
        self.username = username
        image = "icons/default.png"
        if profile_picture_url is not None:
            try:
                img = QImage()
                img.loadFromData(requests.get(profile_picture_url).content)
                image = img
            except:
                pass
        self.profile_picture = image
        self.auth_token = token
        self.email = email


class MainWindow(FramelessWindow):
    def __init__(self, connection, lw):
        super().__init__()
        self.workers = []
        self.threads = []
        self.user = None
        self.stb = StandardTitleBar(self)
        self.stb.setTitle("Taskmaster PRO")
        self.stb.setIcon(QIcon('icons/taskmasterpro.png'))
        self.stb.iconLabel.setStyleSheet("margin:0;padding:0")
        self.setTitleBar(self.stb)
        self.setProperty("MainWindow", True)
        self.resize(820, 534)
        self.setMinimumSize(520, 274)
        self.is_dark = False
        self.mainTabWidget = MainTabWidget(self)
        self.tasks = []
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.connection = connection
        self.lw = lw
        self.setLayout(grid)
        self.titlebar = TitleBar(self)
        self.titlebar.setFixedHeight(74)
        self.titlebar.setContentsMargins(0, 28, 0, 0)
        self.navbar = MainNavbar(self.mainTabWidget, self)
        self.navbar.setFixedWidth(148)
        if self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()
        grid.addWidget(self.titlebar, 0, 1)
        grid.addWidget(self.navbar, 0, 0, 2, 1)
        grid.addWidget(self.mainTabWidget, 1, 1, 1, 1)

        self.login_page = Login(self)
        grid.addWidget(self.login_page, 0, 0, 2, 2)
        self.clockThreadInit()
        self.titleBar.raise_()
        self.show()

    def toggleDarkmode(self):
        if not self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()

    def setDarkMode(self):
        self.setStyleSheet(dark_style_sheet)
        self.is_dark = True
        self.navbar.darkModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.DARK)

    def setLightMode(self):
        self.setStyleSheet(light_style_sheet)
        self.is_dark = False
        self.navbar.lightModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.LIGHT)

    def loadSession(self, data):
        self.user = User(token=data["token"], username=data["user_data"]["username"], email=data["user_data"]["email"])
        self.titlebar.setUserPanel(self.user)
        message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_tasks)

    def set_tasks(self, response: bytes):
        try:
            data = json.loads(response.decode())
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if data["status"] == 403:
            self.logout()
        elif data["status"] == 200:
            self.tasks = []
            for i in data["data"]:
                try:
                    deadline = datetime.strptime(i["DL"], "%Y-%m-%d %H:%M:%S")
                except:
                    deadline = None
                self.tasks.append(
                    Task(i["id"], i["N"], i["T"],
                         datetime.strptime(i["SD"], "%Y-%m-%d %H:%M:%S"),
                         deadline, User(i["ow"]["u"], i["ow"]["e"]),
                         is_owner=i["io"], public=i["pu"], is_completed=i["IC"]))
            self.mainTabWidget.tasksTab.set_tasks(self.tasks)
            self.mainTabWidget.calendarTab.refreshCalendar()

    def set_task_completed(self, pk: int, is_completed: bool):
        message = json.dumps({"url": "/set_completed", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk, "is_completed": is_completed}})
        self.init_send(message.encode(), self.set_task_completed_response)

    def set_task_completed_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            for i in self.tasks:
                if i.id == int(response["data"]["task_id"]):
                    i.is_completed = response["data"]["is_completed"]
                    self.update_tasks()
        elif response["status"] == 403:
            self.logout()

    def delete_task(self, pk: int):
        message = json.dumps({"url": "/delete_task", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk}})
        self.init_send(message.encode(), self.delete_task_response)

    def delete_task_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            for i in self.tasks:
                if i.id == int(response["data"]["task_id"]):
                    message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
                    self.init_send(message.encode(), self.set_tasks)
        elif response["status"] == 403:
            self.logout()

    def delete_tasks(self, pk_list: list):
        message = json.dumps({"url": "/delete_tasks", "method": "POST", "token": self.user.auth_token, "data": {"task_ids": pk_list}})
        self.init_send(message.encode(), self.delete_tasks_response)

    def delete_tasks_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
            self.init_send(message.encode(), self.set_tasks)
        elif response["status"] == 403:
            self.logout()

    def create_task_form(self, date=None):
        self.create_task_dialog = CreateTaskForm(self, date)
        self.create_task_dialog.exec()

    def create_task(self, data: dict):
        message = {"url": "/create_task", "method": "POST", "token": self.user.auth_token}
        message["data"] = data
        message = json.dumps(message)
        self.init_send(message.encode(), self.create_task_response)

    def create_task_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
            if self.create_task_dialog is not None and self.create_task_dialog.isActiveWindow():
                self.create_task_dialog.close()
            self.init_send(message.encode(), self.set_tasks)
        elif response["status"] == 403:
            if self.create_task_dialog is not None and self.create_task_dialog.isActiveWindow():
                self.create_task_dialog.close()
            self.logout()
        elif response["status"] == 401:
            self.create_task_dialog.formError(response["message"])
            self.create_task_dialog.nextB.setDisabled(False)
        elif response["status"] == 400:
            self.create_task_dialog.formError(response["message"])
            self.create_task_dialog.nextB.setDisabled(False)

    def create_user(self, data: dict, func):
        message = {"url": "/create_user", "method": "POST"}
        message["data"] = data
        message = json.dumps(message)
        self.init_send(message.encode(), func)

    def update_tasks(self):
        if self.user is not None:
            change = False
            try:
                for task in self.tasks:
                    if task.update_status():
                        change = True
                if change:
                    self.mainTabWidget.calendarTab.refreshCalendar()
                self.mainTabWidget.tasksTab.update_tasks(change)
            except:
                print("error was raised in the update_tasks function")

    def silent(self, e):
        print(e)
        pass

    def logout(self):
        self.user = None
        self.tasks.clear()
        self.mainTabWidget.tasksTab.set_tasks([])
        self.login_page.fadeIn()

    def attempt_connection(self):
        if self.isVisible():
            self.hide()
        self.connection = None
        self.lw.reconnect()

    def init_view_task_window(self, task_id):
        message = json.dumps({"url": "/task_details", "method": "POST", "token": self.user.auth_token, "data": [task_id]})
        self.init_send(message.encode(), self.view_task)

    def view_task(self, response):
        response = json.loads(response.decode())
        if response["status"] == 200:
            try:
                self.view_task_dialog = ViewTask(self, response["data"][0])
            except:
                return print("Task doesn't exist")
            self.view_task_dialog.exec()
        elif response["status"] == 403:
            self.logout()

    def clockThreadInit(self):
        self.clockThread = QThread()
        self.clockWorker = ClockThread()
        self.clockWorker.moveToThread(self.clockThread)
        self.clockThread.started.connect(self.clockWorker.run)
        self.clockWorker.finished.connect(self.clockThread.quit)
        self.clockWorker.finished.connect(self.clockThread.exit)
        self.clockWorker.finished.connect(self.clockWorker.deleteLater)
        self.clockThread.finished.connect(self.clockThread.deleteLater)
        self.clockWorker.update.connect(self.update_tasks)
        self.clockThread.start()

    def init_send(self, message: bytes, return_function):
        self.threads.append(QThread())
        self.workers.append(SendMessageWorker(self.connection, message))
        thread = self.threads[len(self.threads) - 1]
        worker = self.workers[len(self.workers) - 1]
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(thread.exit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        worker.message.connect(return_function)
        worker.error.connect(self.attempt_connection)
        thread.start()

    def closeEvent(self, event):
        try:
            self.connection.close()
            self.clockThread.exit()
            self.clockWorker.deleteLater()
            self.clockThread.deleteLater()
        except:
            pass
        event.accept()