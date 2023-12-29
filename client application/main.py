import sys
from PyQt5.QtWidgets import QApplication
from connection_window import Application
from config import create_or_read_config

server_address = "192.168.1.48"
server_port = 5240


def main():
    config = create_or_read_config()
    print("settings :", config)
    server_address = config["server_address"]
    server_port = config["server_port"]
    app = QApplication(sys.argv)
    application = Application(server_address, server_port)
    application.connect()
    app.exec()


if __name__ == '__main__':
    sys.exit(main())
