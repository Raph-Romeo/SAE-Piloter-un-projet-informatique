from qframelesswindow import FramelessDialog
import socket
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QColor
import time
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from main_window import MainWindow
from qfluentwidgets import PushButton, LineEdit, SubtitleLabel, setThemeColor, setTheme, Theme
from config import create_or_read_config, edit_config
from color_icon import color_pixmap


class ConnectionWorker(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(str)
    return_signal = pyqtSignal(object)

    def __init__(self, address: str, port: int, retry: bool=False):
        super().__init__()
        self.connection = None
        self.address = address
        self.port = port
        self.retry = retry

    def run(self):
        self.connection = socket.socket()
        self.connection.settimeout(5)
        if not self.retry:
            self.message.emit("Connecting to server...")
            try:
                self.connection.connect((self.address, self.port))
                self.return_signal.emit(self.connection)
            except:
                pass
        else:
            self.message.emit("Could not connect to server.\nTrying again in 5 seconds")
            time.sleep(1)
            self.message.emit("Could not connect to server.\nTrying again in 4 seconds")
            time.sleep(1)
            self.message.emit("Could not connect to server.\nTrying again in 3 seconds")
            time.sleep(1)
            self.message.emit("Could not connect to server.\nTrying again in 2 seconds")
            time.sleep(1)
            self.message.emit("Could not connect to server.\nTrying again in 1 seconds")
            time.sleep(1)
        self.finished.emit()


class Application(FramelessDialog):
    def __init__(self, address: str, port: int):
        super().__init__()
        self.titleBar.hide()
        config = create_or_read_config()
        self.address = config["server_address"]
        self.port = config["server_port"]
        self.appWindow = None
        self.connection = None
        self.setResizeEnabled(False)
        self.setFixedSize(300, 350)
        self.suspended_timeout = False
        layout = QVBoxLayout(self)
        self.label = QLabel("Loading app...")
        pixmap = QPixmap("icons/calendrier.png")
        pixmap = pixmap.scaled(100, 100)
        self.icon = QLabel(self)
        self.icon.setPixmap(pixmap)
        self.icon.setFixedHeight(180)
        self.icon.setFixedWidth(200)
        self.icon.setAlignment(Qt.AlignCenter)
        layout.setAlignment(Qt.AlignCenter)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(60)
        self.label.setFixedWidth(200)
        self.label.setStyleSheet("font-size:12px;font-family:verdana;")
        self.configLabel = QLabel()
        self.configLabel.setText("Connection config")
        self.configLabel.setAlignment(Qt.AlignCenter)
        self.configLabel.setStyleSheet("font-size:14px;font-family:verdana;")
        self.configLabel.setHidden(True)
        self.addressLabel = QLabel("Server address :")
        self.addressLabel.setStyleSheet("font-size:12px;font-family:verdana;")
        self.addressLabel.setHidden(True)
        self.portLabel = QLabel("Server port :")
        self.portLabel.setStyleSheet("font-size:12px;font-family:verdana;")
        self.portLabel.setHidden(True)
        self.editServerConfigButton = PushButton()
        self.editServerConfigButton.setText("Edit connection config")
        self.editServerConfigButton.setHidden(True)
        self.editServerConfigButton.clicked.connect(self.edit_connection_config_window_toggle)
        self.editServerConfigWindowOpen = False
        self.serverAddressLineEdit = LineEdit()
        self.serverAddressLineEdit.setPlaceholderText("Server address or domain")
        self.serverAddressLineEdit.setHidden(True)
        self.serverPortLineEdit = LineEdit()
        self.serverPortLineEdit.setPlaceholderText("Server port")
        self.serverPortLineEdit.setHidden(True)
        
        self.set_theme(config["theme"])
        setThemeColor("#5b2efc")
        
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        layout.addWidget(self.configLabel)
        layout.addWidget(self.addressLabel)
        layout.addWidget(self.serverAddressLineEdit)
        layout.addWidget(self.portLabel)
        layout.addWidget(self.serverPortLineEdit)
        layout.addWidget(self.editServerConfigButton)

    def setText(self, txt: str):
        self.label.setText(txt)

    def connect(self):
        if self.connection is not None:
            self.connection = None
        self.editServerConfigButton.setDisabled(True)
        self.show()
        self.thread = QThread()
        self.worker = ConnectionWorker(self.address, self.port)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.check_connection_status)
        self.worker.message.connect(self.setText)
        self.worker.return_signal.connect(self.saveConnection)
        self.thread.start()
    
    def check_connection_status(self):
        if self.connection is None:
            return self.reconnect_timeout()
        else:
            return

    def reconnect_timeout(self):
        self.editServerConfigButton.setDisabled(False)
        self.editServerConfigButton.setHidden(False)
        self.show()
        self.thread = QThread()
        self.worker = ConnectionWorker(self.address, self.port, retry=True)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.reconnect_attempt)
        self.worker.message.connect(self.setText)
        self.thread.start()

    def reconnect_attempt(self):
        if not self.editServerConfigWindowOpen:
            self.connect()
        else:
            self.suspended_timeout = True
            self.setText("User is editing config...")

    def load_app(self):
        self.setText("Loading widgets...")
        self.appWindow = MainWindow(self.connection, self)
        self.renderAW()

    def set_theme(self, theme=None):
        if self.appWindow is not None:
            if self.appWindow.is_dark:
                self.setStyleSheet("background:#222;color:white")
                #self.label.setStyleSheet("color:white")
                #self.label.setStyleSheet("color:white")
                pixmap = color_pixmap("icons/calendrier.png", QColor(255, 255, 255))
                pixmap = pixmap.scaled(100, 100)
                self.icon.setPixmap(pixmap)
            else:
                self.setStyleSheet("background:#EEE;color:black")
                #self.label.setStyleSheet("color:black")
                pixmap = QPixmap("icons/calendrier.png")
                pixmap = pixmap.scaled(100, 100)
                self.icon.setPixmap(pixmap)
        elif theme == 0:
            self.setStyleSheet("background:#EEE;color:black")
            #self.label.setStyleSheet("color:black")
            pixmap = QPixmap("icons/calendrier.png")
            pixmap = pixmap.scaled(100, 100)
            self.icon.setPixmap(pixmap)
            setTheme(Theme.LIGHT)
        else:
            self.setStyleSheet("background:#222;color:white")
            #self.label.setStyleSheet("color:white")
            pixmap = color_pixmap("icons/calendrier.png", QColor(255, 255, 255))
            pixmap = pixmap.scaled(100, 100)
            self.icon.setPixmap(pixmap)
            setTheme(Theme.DARK)

    def renderAW(self):
        self.appWindow.show()
        self.hide()

    def saveConnection(self, connection):
        self.editServerConfigButton.setHidden(True)
        self.connection = connection
        if self.appWindow is not None:
            self.appWindow.connection = self.connection
            self.renderAW()
        else:
            self.load_app()

    def edit_connection_config_window_toggle(self):
        if self.editServerConfigWindowOpen:
            self.editServerConfigWindowOpen = False
            if self.suspended_timeout:
                self.suspended_timeout = False
                self.connect()
            self.icon.setHidden(False)
            self.serverPortLineEdit.setHidden(True)
            self.serverAddressLineEdit.setHidden(True)
            self.configLabel.setHidden(True)
            self.portLabel.setHidden(True)
            self.addressLabel.setHidden(True)
            self.label.setHidden(False)
            self.editServerConfigButton.setText("Edit connection config")
            try:
                if self.address != self.serverAddressLineEdit.text():
                    self.address = self.serverAddressLineEdit.text()
                    edit_config("Settings.server_address", str(self.address))
            except:
                pass
            try:
                if self.port != int(self.serverPortLineEdit.text()):
                    self.port = int(self.serverPortLineEdit.text())
                    edit_config("Settings.server_port", str(self.port))
            except:
                pass
        else:
            config = create_or_read_config()
            self.icon.setHidden(True)
            self.label.setHidden(True)
            self.configLabel.setHidden(False)
            self.serverAddressLineEdit.setHidden(False)
            self.serverPortLineEdit.setHidden(False)
            self.portLabel.setHidden(False)
            self.addressLabel.setHidden(False)
            self.serverAddressLineEdit.setText(config["server_address"])
            self.serverPortLineEdit.setText(str(config["server_port"]))
            self.editServerConfigWindowOpen = True
            self.editServerConfigButton.setText("Save config")
