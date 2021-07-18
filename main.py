import sys

from PyQt5 import QtWidgets

from modules.MainWindow.MainWindow import MainWindow


if __name__ == "__main__":
    config_path = "config.ini"

    app = QtWidgets.QApplication([])
    application = MainWindow(config_path=config_path)
    application.show()

    sys.exit(app.exec())


