from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from stylesheets import dark_style_sheet, light_style_sheet
from navbar import MainNavbar
from tab_widgets import MainTabWidget
from titlebar import TitleBar
from qframelesswindow import FramelessWindow, StandardTitleBar
from login import Login
from qfluentwidgets import setTheme, Theme, InfoBar, InfoBarPosition, setThemeColor
from datetime import datetime, timedelta
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from view_task import ViewTask
import errno
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

    def __init__(self, connection, message: bytes, use_original_socket=False):
        super().__init__()
        self.connection = connection
        self.msg = message
        self.use_original_socket = use_original_socket

    def run(self):
        try:
            if self.use_original_socket:
                try:
                    self.connection.send(self.msg)
                    data = self.connection.recv(1024)
                    self.message.emit(data)
                except Exception as err:
                    print("Testing conn error : ", err)
                    self.raise_socket_error()
                return self.finished.emit()
            else:
                remote_ip, remote_port = self.connection.getpeername()
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((remote_ip, remote_port))
                conn.setblocking(False)
                conn.send(self.msg)
                data = b""
                while True:
                    try:
                        chunk = conn.recv(1024)  # Receive data in chunks
                        data += chunk
                        if data != b"" and chunk is None:
                            self.raise_socket_error()
                            break
                    except socket.error as e:
                        err_code = e.errno
                        if err_code == errno.WSAEWOULDBLOCK:
                            pass
                        else:
                            self.raise_socket_error()
                            break
                    try:
                        if data != b"":
                            json.loads(data.decode())
                            self.message.emit(data)
                            break
                    except:
                        pass
                conn.close()
        except Exception as err:
            print("CONNECTION ERROR WITH SERVER : ", err)
            self.raise_socket_error()
            return self.finished.emit()

    def raise_socket_error(self):
        self.error.emit()
        response = json.dumps({"status": 0}).encode()
        self.message.emit(response)


class ClockThread(QObject):
    finished = pyqtSignal()
    update = pyqtSignal()
    testConnection = pyqtSignal()
    fetchRequests = pyqtSignal()
    count = 0

    def run(self):
        while True:
            time.sleep(1)
            self.count += 1
            self.update.emit()
            if self.count == 5 or self.count == 10:
                self.testConnection.emit()
            elif self.count == 15:
                self.fetchRequests.emit()
                self.count = 0


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
    def __init__(self, username, email, first_name=None, last_name=None, profile_picture_url=None, token=None):
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
        self.first_name = first_name
        self.last_name = last_name


class Friend:
    def __init__(self, username, email, first_name, last_name, request_id):
        self.id = request_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class MainWindow(FramelessWindow):
    def __init__(self, connection, lw):
        super().__init__()
        self.fetchingRequests = False
        self.current_view_task_dialog = None
        self.number_of_friend_requests = 0
        self.workers = []
        self.threads = []
        self.friends = []
        setThemeColor("#5b2efc")
        self.user = None
        self.create_task_dialog = None
        self.view_task_dialogs = []
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
        message = json.dumps({"url": "/friends", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_friends)

    def set_friends(self, response):
        try:
            data = json.loads(response.decode())
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if data["status"] == 200:
            self.friends = []
            for i in data["data"]["friends"]:
                try:
                    self.friends.append(Friend(username=i["u"], email=i["e"], first_name=i["fn"], last_name=i["ln"], request_id=i["request_id"]))
                except Exception as err:
                    print("failed to create friend object", err)
            self.mainTabWidget.friendsTab.set_friends(self.friends)
            self.mainTabWidget.friendsTab.refreshFriendsButton.setDisabled(False)

    # This method is subject to change. Only a temporary solution
    def remove_tasks(self, task_ids: list):
        tasks = []
        for task in self.tasks:
            if task.id not in task_ids:
                tasks.append(task)
        self.mainTabWidget.tasksTab.contentWindow.remove_tasks(task_ids)
        self.tasks = tasks
        self.mainTabWidget.calendarTab.refreshCalendar()

    def add_task(self, task):
        try:
            deadline = datetime.strptime(task["DL"], "%Y-%m-%d %H:%M:%S")
        except:
            deadline = None
        new_task = Task(task["id"], task["N"], task["T"],datetime.strptime(task["SD"], "%Y-%m-%d %H:%M:%S"),deadline, User(task["ow"]["u"], task["ow"]["e"]),is_owner=task["io"], public=task["pu"], is_completed=task["IC"])
        self.tasks.insert(0, new_task)
        self.mainTabWidget.tasksTab.contentWindow.add_task(new_task)
        self.mainTabWidget.calendarTab.refreshCalendar()

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
            self.mainTabWidget.tasksTab.set_tasks()
            self.mainTabWidget.calendarTab.refreshCalendar()

    def set_task_completed(self, pk: int, is_completed: bool):
        message = json.dumps({"url": "/set_completed", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk, "is_completed": is_completed}})
        self.init_send(message.encode(), self.set_task_completed_response)

    def set_task_completed_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            if response["data"]["is_completed"]:
                InfoBar.info(title="", content="Set task to completed", parent=self, orient=Qt.Horizontal, isClosable=False, position=InfoBarPosition.TOP_RIGHT, duration=1000)
            else:
                InfoBar.info(title="", content="Set task to incomplete", parent=self, orient=Qt.Horizontal, isClosable=False, position=InfoBarPosition.TOP_RIGHT, duration=1000)
            for i in self.tasks:
                if i.id == int(response["data"]["task_id"]):
                    i.is_completed = response["data"]["is_completed"]
                    break
            self.update_tasks()
            if self.current_view_task_dialog is not None:
                try:
                    if self.current_view_task_dialog.isActiveWindow():
                        if self.current_view_task_dialog.task_id == int(response["data"]["task_id"]):
                            self.current_view_task_dialog.disableStatusUpdate = True
                            self.current_view_task_dialog.changeStatus(response["data"]["is_completed"])
                except:
                    pass
        elif response["status"] == 403:
            self.logout()
        elif response["status"] == 404:
            self.remove_tasks([response["data"]["task_id"]])
            InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)

    def delete_task(self, pk: int):
        message = json.dumps({"url": "/delete_task", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk}})
        self.init_send(message.encode(), self.delete_task_response)

    def delete_task_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            InfoBar.info(title="", content="Deleted task", parent=self, orient=Qt.Horizontal, isClosable=False, position=InfoBarPosition.TOP_RIGHT, duration=1000)
            self.remove_tasks([int(response["data"]["task_id"])])
        elif response["status"] == 403:
            self.logout()
        elif response["status"] == 404:
            self.remove_tasks([int(response["data"]["task_id"])])
            InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)

    def delete_tasks(self, pk_list: list):
        message = json.dumps({"url": "/delete_tasks", "method": "POST", "token": self.user.auth_token, "data": {"task_ids": pk_list}})
        self.init_send(message.encode(), self.delete_tasks_response)

    def delete_tasks_response(self, e):
        response = json.loads(e.decode())
        if response["status"] == 200:
            for task in response["data"]["tasks"]:
                if task["status"] == 200:
                    InfoBar.info(title="", content="Deleted task", parent=self, orient=Qt.Horizontal, isClosable=False, position=InfoBarPosition.TOP_RIGHT, duration=1000)
                elif task["status"] == 404:
                    InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            self.remove_tasks(response["data"]["task_ids"])
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
            InfoBar.success(title="Created task", content=f'{response["data"]["task"]["N"]}', parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
            if self.create_task_dialog is not None and self.create_task_dialog.isActiveWindow():
                self.create_task_dialog.close()
            self.add_task(response["data"]["task"])
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
        elif response["status"] == 0:
            if self.create_task_dialog is not None and self.create_task_dialog.isActiveWindow():
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
        print("[ KEEP ALIVE ] - Testing conn")
        pass

    def logout(self):
        self.user = None
        self.tasks.clear()
        self.number_of_friend_requests = 0
        self.friends.clear()
        self.mainTabWidget.friendsTab.clear_friends()
        self.mainTabWidget.tasksTab.set_tasks()
        self.login_page.fadeIn()

    def attempt_connection(self):
        if self.connection is not None:
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
                if "not_found" in response["data"][0].keys():
                    self.remove_tasks([response["data"][0]["id"]])
                    return InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
                self.view_task_dialogs.append(ViewTask(self, response["data"][0]))
                view_task_dialog = self.view_task_dialogs[len(self.view_task_dialogs) - 1]
                self.current_view_task_dialog = view_task_dialog
                view_task_dialog.exec()
            except:
                return InfoBar.error(title="Error", content="Could not fetch task details", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
        elif response["status"] == 403:
            self.logout()

    def init_edit_task_window(self, task_id):
        message = json.dumps({"url": "/task_details", "method": "POST", "token": self.user.auth_token, "data": [task_id]})
        self.init_send(message.encode(), self.edit_task)

    def edit_task(self, response):
        response = json.loads(response.decode())
        if response["status"] == 200:
            try:
                if "not_found" in response["data"][0].keys():
                    self.remove_tasks([response["data"][0]["id"]])
                    return InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
                self.view_task_dialogs.append(ViewTask(self, response["data"][0]))
                view_task_dialog = self.view_task_dialogs[len(self.view_task_dialogs) - 1]
                self.current_view_task_dialog = view_task_dialog
                view_task_dialog.exec()
            except:
                return InfoBar.error(title="Error", content="Could not fetch task details", parent=self,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT,duration=5000)

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
        self.clockWorker.testConnection.connect(self.testConnection)
        self.clockWorker.fetchRequests.connect(self.fetchRequests)
        self.clockThread.start()

    def init_send(self, message: bytes, return_function, use_original_socket=False):
        if self.connection is not None:
            self.threads.append(QThread())
            self.workers.append(SendMessageWorker(self.connection, message, use_original_socket))
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
            #for worker in self.workers:
            #    try:
            #        worker.quit()
            #    except Exception as err:
            #        print(f"Failed to close worker {worker}")
            #        print(f"with error {err}")
        except:
            pass
        event.accept()

    def testConnection(self):
        if self.connection is not None:
            self.init_send(json.dumps({"t": 1}).encode(), self.silent, True)

    def fetchRequests(self):
        if self.connection is not None:
            if self.user is not None and not self.fetchingRequests:
                self.fetchingRequests = True
                message = json.dumps({"url": "/fetch_requests", "method": "GET", "token": self.user.auth_token})
                return self.init_send(message.encode(), self.fetchRequestsResponse, True)
            else:
                return self.testConnection()

    def fetchRequestsResponse(self, response: bytes):
        self.fetchingRequests = False
        try:
            data = json.loads(response.decode())
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if self.user is not None:
            if data["status"] == 200:
                if self.number_of_friend_requests != int(data["data"]["request_num"]):
                    if self.number_of_friend_requests > int(data["data"]["request_num"]):
                        self.update_friends()
                    self.number_of_friend_requests = int(data["data"]["request_num"])
                    self.mainTabWidget.friendsTab.set_friend_requests(self.number_of_friend_requests)
                    if self.number_of_friend_requests > 0:
                        return InfoBar.info(title="Friend request", content=f"You have {self.number_of_friend_requests} pending friend requests !", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=10000)
                    else:
                        return
                if len(self.friends) != int(data["data"]["number_of_friends"]):
                    self.update_friends()
                    return
            elif data["status"] == 400:
                return
        else:
            return

    def update_friends(self):  # refresh friends...
        message = json.dumps({"url": "/friends", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_friends)

    def refresh_tasks(self):
        InfoBar.info(title="", content="Refreshing tasks...", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=2000)
        self.mainTabWidget.tasksTab.contentWindow.refreshTasksButton.setDisabled(True)
        message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_tasks)
