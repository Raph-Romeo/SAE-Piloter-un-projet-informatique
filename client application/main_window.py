from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from stylesheets import dark_style_sheet, light_style_sheet
from navbar import MainNavbar
from tab_widgets import MainTabWidget
from titlebar import TitleBar
from qframelesswindow import FramelessWindow, StandardTitleBar
from login import Login
from qfluentwidgets import setTheme, Theme, InfoBar, InfoBarPosition
from datetime import datetime, timedelta
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from view_task import ViewTask
import errno
import time
import socket
import requests
import json
from config import create_or_read_config
from create_task import CreateTaskForm
from user_profile import AccountProfile


class SendMessageWorker(QObject):
    """
    This class is used as a worker for a thread.
    It essentially handles the message sending through the socket in the server, given that this action is blocking
    (Waiting for the response) we use a thread to handle this.
    """
    # When the thread finishes, the finished signal gets called.
    finished = pyqtSignal()
    # When the message response is received from the socket, we use the message signal to send it back to the main
    # thread.
    message = pyqtSignal(bytes)
    # If an error occurs with the socket, the error signal is used to warn the main thread.
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
    """
        This class is used as a worker for a thread.
        As the name suggests, it acts as a clock for anything in the application.
        We can calculate the task's time left in real time thanks to this timer, and also, we are initiating connection
        test every 5 seconds.
    """
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
    """
        This class is used to create a Task object containing all the task's information.
        It also includes a few methods to allow us to easily determine the task's status and the time left before the deadline is reached.
    """
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
    """
     The current user for the application is defined with this class.
     It contains the auth_token that is necessary to maintain a valid authentication with the server.
    """
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
    """
    Main window of the application.
    Most of the methods and attributes defined are fundamental for the application.
    """
    def __init__(self, connection, lw):
        super().__init__()
        # This attribute contains the dialog window for viewing a user's profile.
        self.account_profile_dialog = None
        # This boolean attribute indicates whether if we are currently fetching requests or not. This is useful
        # to avoid a potential crash, where the server response is very delayed.
        self.fetchingRequests = False
        # This attribute contains the object for the dialog window when viewing a task's details.
        self.current_view_task_dialog = None
        self.view_task_dialogs = []
        # This contains the number of current pending received friend requests.
        self.number_of_friend_requests = 0
        # The following lists are used to store the current running threads.
        self.workers = []
        self.threads = []
        # This list contains all the active user's tasks as objects from the Task class.
        self.tasks = []
        # This list contains all the active user's friends as objects from the Friend class.
        self.friends = []
        # This attribute contains the active User object from the User class.
        self.user = None
        # This attribute contains the task creation dialog object.
        self.create_task_dialog = None

        # Creation of the application window
        self.stb = StandardTitleBar(self)
        self.stb.setTitle("Taskmaster PRO")
        self.stb.setIcon(QIcon('icons/taskmasterpro.png'))
        self.stb.iconLabel.setStyleSheet("margin:0;padding:0")
        self.setTitleBar(self.stb)
        self.setProperty("MainWindow", True)
        self.resize(820, 534)
        self.setMinimumSize(520, 274)

        # Obtaining the settings values from the config file.
        settings = create_or_read_config()
        # Setting the is_dark attribute to true if the config file has dark mode set to true, else to false.
        if settings["theme"] == 1:
            self.is_dark = True
        elif settings["theme"] == 0:
            self.is_dark = False
        # Applying the column auto resizing if the settings in the config file are set to auto resize.
        if settings["auto_resize_columns"] == 1:
            self.autoResizeColumns = True
        else:
            self.autoResizeColumns = False
        # Creating the main tab widget tab for the app. This is the widget that holds all the main tabs of the app.
        self.mainTabWidget = MainTabWidget(self)

        # Defining the grid layout of the main Window.
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)

        # Defining the socket connection attribute.
        self.connection = connection

        # lw stands for loading window. It is the object reference of the window that appears when the app is loading.
        self.lw = lw

        # Defining the titlebar widget of the app.
        self.titlebar = TitleBar(self)
        self.titlebar.setFixedHeight(74)
        self.titlebar.setContentsMargins(0, 28, 0, 0)

        # Defining the left side navbar of the app.
        self.navbar = MainNavbar(self.mainTabWidget, self)
        self.navbar.setFixedWidth(148)

        # Applying the dark theme or light theme depending on the state of the self.is_dark attribute
        if self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()

        # Adding the widgets to the layout of the window.
        grid.addWidget(self.titlebar, 0, 1)
        grid.addWidget(self.navbar, 0, 0, 2, 1)
        grid.addWidget(self.mainTabWidget, 1, 1, 1, 1)

        # Creating the login page and overlaying it on the main window layout.
        self.login_page = Login(self)
        grid.addWidget(self.login_page, 0, 0, 2, 2)

        # Calling clockThreadInit method.
        self.clockThreadInit()

        # Calling titlebar raise method which initiates the custom titlebar for the Fluent-Frameless-Window object.
        self.titleBar.raise_()

        # Rendering the window once setup is complete
        self.show()

    def toggleDarkmode(self):
        """
        Simple switch function to toggle dark mode if it is not currently set, or vise versa.
        """
        if not self.is_dark:
            self.setDarkMode()
        else:
            self.setLightMode()

    def setDarkMode(self):
        """
        Setting dark theme to the application.
        Changing style sheet and changing icon colors.
        """
        self.setStyleSheet(dark_style_sheet)
        self.is_dark = True
        self.navbar.darkModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.DARK)

    def setLightMode(self):
        """
        Setting light theme to the application.
        Changing style sheet and changing icon colors.
        """
        self.setStyleSheet(light_style_sheet)
        self.is_dark = False
        self.navbar.lightModeIcons()
        self.stb.closeBtn.setHoverColor(QColor(255, 255, 255))
        self.stb.closeBtn.setPressedColor(QColor(255, 255, 255))
        self.stb.closeBtn.setHoverBackgroundColor(QColor(232, 17, 35))
        self.stb.closeBtn.setPressedBackgroundColor(QColor(241, 112, 122))
        setTheme(Theme.LIGHT)

    def loadSession(self, data):
        """
        Loading the user session, handling the authentication process and fetching all the user's data, including:
         - User's profile.
         - User's authentication token.
         - User's tasks.
         - User's friends.
        """
        self.user = User(token=data["token"], username=data["user_data"]["username"], first_name=data["user_data"]["first_name"], last_name=data["user_data"]["last_name"], email=data["user_data"]["email"])
        self.titlebar.setUserPanel(self.user)
        message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_tasks)
        message = json.dumps({"url": "/friends", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_friends)

    def set_friends(self, response):
        """
        Sets friends to the server's response of the user's friend list.
        """
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

    def remove_tasks(self, task_ids: list):
        """
        Remove tasks from task list, and from the calendar from a list of task IDs.
        """
        tasks = []
        for task in self.tasks:
            if task.id not in task_ids:
                tasks.append(task)
        self.mainTabWidget.tasksTab.contentWindow.remove_tasks(task_ids)
        self.tasks = tasks
        self.mainTabWidget.calendarTab.refreshCalendar()

    def add_task(self, task):
        """
        Add task to the calendar and to the task list.
        """
        try:
            deadline = datetime.strptime(task["DL"], "%Y-%m-%d %H:%M:%S")
        except:
            deadline = None
        new_task = Task(task["id"], task["N"], task["T"],datetime.strptime(task["SD"], "%Y-%m-%d %H:%M:%S"),deadline, User(task["ow"]["u"], task["ow"]["e"]),is_owner=task["io"], public=task["pu"], is_completed=task["IC"])
        self.tasks.insert(0, new_task)
        self.mainTabWidget.tasksTab.contentWindow.add_task(new_task)
        self.mainTabWidget.calendarTab.refreshCalendar()

    def set_tasks(self, response: bytes):
        """
        Remove all tasks (if any), and set them to the server's response of the user's list of tasks.
        """
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
        """
        Send the request to the server to set a task to completed status or to incomplete status with arguments:
         - pk > int ID of the task we want to change the completion status of.
         - is_completed > bool completion status of the task.
        """
        message = json.dumps({"url": "/set_completed", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk, "is_completed": is_completed}})
        self.init_send(message.encode(), self.set_task_completed_response)

    def set_task_completed_response(self, e):
        """
        Handling server response from the completion status change of the task.
        """
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
        """
        Send the request to the server to delete a task with argument:
         - pk > int ID of the task.
        """
        message = json.dumps({"url": "/delete_task", "method": "POST", "token": self.user.auth_token, "data": {"task_id": pk}})
        self.init_send(message.encode(), self.delete_task_response)

    def delete_task_response(self, e):
        """
        Handling the server response from deleting a task.
        """
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
        """
        Send the request to the server to delete multiple tasks with argument:
         - pk_list > list IDs of the tasks.
        """
        message = json.dumps({"url": "/delete_tasks", "method": "POST", "token": self.user.auth_token, "data": {"task_ids": pk_list}})
        self.init_send(message.encode(), self.delete_tasks_response)

    def delete_tasks_response(self, e):
        """
        Handling the server response from deleting multiple tasks.
        """
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
        """
        Display the create task form dialog. With optional argument:
        - date > datetime object, default date for the create task form.
        """
        self.create_task_dialog = CreateTaskForm(self, date)
        self.create_task_dialog.exec()

    def view_account_profile(self, user):
        """
        Display the active user's profile.
        """
        self.account_profile_dialog = AccountProfile(self, user)
        self.account_profile_dialog.exec()

    def create_task(self, data: dict):
        """
        Send the request to the server to create a task with argument:
         - data > dict object, containing the relevant information for the task we wish to create.
        """
        message = {"url": "/create_task", "method": "POST", "token": self.user.auth_token}
        message["data"] = data
        message = json.dumps(message)
        self.init_send(message.encode(), self.create_task_response)

    def create_task_response(self, e):
        """
        Handle the server response from the task creation request.
        """
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
        """
        Send the request to the server to create a user account with argument:
         - data > dict object, containing the relevant information for the user account we wish to create.
        """
        message = {"url": "/create_user", "method": "POST"}
        message["data"] = data
        message = json.dumps(message)
        self.init_send(message.encode(), func)

    def update_tasks(self):
        """
         Force the tasks to update in the calendar and in the task list.
         Update consists of :
         real time -> task time left display.
         real time -> task current status.
        """
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
        """
        This method is used to dispose of any unneeded response from the server
        """
        print("[ KEEP ALIVE ] - Testing conn")
        pass

    def logout(self):
        """
        This method is used to handle the logout, and clearing all user data.
        """
        self.user = None
        self.tasks.clear()
        self.number_of_friend_requests = 0
        self.friends.clear()
        self.mainTabWidget.friendsTab.clear_friends()
        self.mainTabWidget.tasksTab.set_tasks()
        self.login_page.fadeIn()

    def attempt_connection(self):
        """
        This method is called upon when an error is raised from the sendMessageWorker thread, and it will basically
        attempt to reconnect to the server.
        """
        if self.connection is not None:
            if self.isVisible():
                self.hide()
            self.connection = None
            self.lw.reconnect_attempt()
            self.lw.set_theme()

    def init_view_task_window(self, task_id):
        """
        Before creating the task view dialog (containing all the task's information), we send a request to the server to
        obtain all the information details from the task using the task_id argument.
        args :
        task_id > INT task_id contains the ID of the task.
        """
        message = json.dumps({"url": "/task_details", "method": "POST", "token": self.user.auth_token, "data": [task_id]})
        self.init_send(message.encode(), self.view_task)

    def view_task(self, response):
        """
        Creating the task view dialog, handling the server's response containing all the task's information.
        """
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
        """
        Before creating the task edit dialog, we send a request to the server to
        obtain all the information details from the task thanks to the task_id argument.
        args :
        task_id > INT task_id contains the ID value of the task.
        """
        message = json.dumps({"url": "/task_details", "method": "POST", "token": self.user.auth_token, "data": [task_id]})
        self.init_send(message.encode(), self.edit_task)

    def edit_task(self, response):
        """
        Creating the task edit dialog, handling the server's response containing all the task's information.
        """
        response = json.loads(response.decode())
        if response["status"] == 200:
            try:
                if "not_found" in response["data"][0].keys():
                    self.remove_tasks([response["data"][0]["id"]])
                    return InfoBar.warning(title="404", content="Task not found", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=5000)
                self.view_task_dialogs.append(ViewTask(self, response["data"][0], edit_mode=True))
                view_task_dialog = self.view_task_dialogs[len(self.view_task_dialogs) - 1]
                self.current_view_task_dialog = view_task_dialog
                view_task_dialog.exec()
            except:
                return InfoBar.error(title="Error", content="Could not fetch task details", parent=self,orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT,duration=5000)

        elif response["status"] == 403:
            self.logout()

    def clockThreadInit(self):
        """
        Creating the application's clock thread object.
        """
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
        """
        INITIATING THE MESSAGE SENDING THREAD TO THE SERVER.
        Arguments:
        message -> Bytes,JSON message containing the data that we wish to send to the server (url+data+auth+etc...)
        return_function -> reference to the return function into which we will provide the server's response.
        user_original_socket -> Do we wish to create a new connection socket for this message, or not.
        """
        # Making sure that the self.connection attribute is not None.
        # It will be None in the case where we have temporarily lost connection with the server.
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
        """
        Handling of the closing of the application's main window.
        """
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
        """
        Sending the server a "test" request identified by the json message : {"t": 1} which is essentially only used
        to keep testing the status of the connection. If the connection to the server is abruptly lost,
        the application will be aware of this, and instantly attempt to reconnect to the server and keep retrying
        until it succeeds.
        Trivia : This behaviour was inspired from the desktop application of discord.
        """
        if self.connection is not None:
            self.init_send(json.dumps({"t": 1}).encode(), self.silent, True)

    def fetchRequests(self):
        """
        Sending the server a fetch request in order to test to see if there is a difference between the client's data
        and the server.
        This will additionally allow the client to instantly notify the user if a friend request was received.
        """
        if self.connection is not None:
            if self.user is not None and not self.fetchingRequests:
                self.fetchingRequests = True
                message = json.dumps({"url": "/fetch_requests", "method": "GET", "token": self.user.auth_token})
                return self.init_send(message.encode(), self.fetchRequestsResponse, True)
            else:
                return self.testConnection()

    def fetchRequestsResponse(self, response: bytes):
        """
        Handling the fetch request response from the server.
        """
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
        """
        Refreshing client's active user's friends.
        Sending a request to the server to get all the active user's friends and then setting them to the friend list table.
        """
        message = json.dumps({"url": "/friends", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_friends)

    def refresh_tasks(self):
        """
        Refreshing client's active user's tasks.
        Sending a request to the server to get all the active user's tasks and then setting them to the calendar and task list table.
        """
        InfoBar.info(title="", content="Refreshing tasks...", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=2000)
        self.mainTabWidget.tasksTab.contentWindow.refreshTasksButton.setDisabled(True)
        message = json.dumps({"url": "/tasks", "method": "GET", "token": self.user.auth_token})
        self.init_send(message.encode(), self.set_tasks)

    def unfriend(self, request_id):
        """
        Sending a request to the server to unfriend a user with argument:
        request_id > INT ID of the friendship request.
        """
        message = json.dumps({"url": "/unfriend", "method": "POST", "token": self.user.auth_token, "data": {"request_id": request_id}})
        self.init_send(message.encode(), self.unfriend_response)

    def unfriend_response(self, response):
        """
        Handling the unfriend response from the server.
        """
        try:
            data = json.loads(response.decode())
        except:
            return print(f"error decoding tasks message : {response.decode()}")
        if data["status"] == 200:
            InfoBar.info(title="", content="Removed friend", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=2000)
            self.update_friends()
        elif data["status"] == 404:
            InfoBar.info(title="", content="You are not friends with this user", parent=self, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT, duration=2000)
            self.update_friends()