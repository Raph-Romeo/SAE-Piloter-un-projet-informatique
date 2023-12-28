from qframelesswindow import FramelessDialog
import socket
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import time
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from main_window import MainWindow


class ConnectionWorker(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(str)
    return_signal = pyqtSignal(object)

    def __init__(self, address: str, port: int):
        super().__init__()
        self.connection = None
        self.address = address
        self.port = port

    def run(self):
        self.connection = socket.socket()
        self.connection.settimeout(5)
        self.message.emit("Connecting to server...")
        try:
            self.connection.connect((self.address, self.port))
            self.return_signal.emit(self.connection)
        except:
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
            self.run()
        self.finished.emit()


class Application(FramelessDialog):
    def __init__(self, address: str, port: int):
        super().__init__()
        self.titleBar.hide()
        self.appWindow = None
        self.connection = None
        self.setResizeEnabled(False)
        self.setFixedSize(300, 350)
        self.address = address
        self.port = port
        layout = QVBoxLayout(self)
        self.label = QLabel("Loading app...")
        pixmap = QPixmap("icons/calendrier.png")
        pixmap = pixmap.scaled(100, 100)
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setFixedHeight(180)
        icon.setFixedWidth(200)
        icon.setAlignment(Qt.AlignCenter)
        layout.setAlignment(Qt.AlignCenter)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(60)
        self.label.setFixedWidth(200)
        self.label.setStyleSheet("font-size:12px;font-family:verdana;")
        layout.addWidget(icon)
        layout.addWidget(self.label)

    def setText(self, txt: str):
        self.label.setText(txt)

    def connect(self):
        self.show()
        self.thread = QThread()
        self.worker = ConnectionWorker(self.address, self.port)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.message.connect(self.setText)
        self.worker.return_signal.connect(self.saveConnection)
        self.thread.finished.connect(self.load_app)
        self.thread.start()

    def reconnect(self):
        self.show()
        self.thread = QThread()
        self.worker = ConnectionWorker(self.address, self.port)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.message.connect(self.setText)
        self.worker.return_signal.connect(self.updateConnection)
        self.thread.start()

    def load_app(self):
        self.setText("Loading widgets...")
        self.appWindow = MainWindow(self.connection, self)
        self.renderAW()

    def renderAW(self):
        self.appWindow.show()
        self.hide()

    def saveConnection(self, connection):
        self.connection = connection

    def updateConnection(self, connection):
        self.saveConnection(connection)
        self.appWindow.connection = self.connection
        self.renderAW()
