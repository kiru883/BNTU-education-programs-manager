import PyQt5

from PyQt5.QtWidgets import QMessageBox, QAbstractButton


class MessageBox(QMessageBox):
    def __init__(self):
        # init
        super(MessageBox, self).__init__()
        # setup
        self.setIcon(QMessageBox.Warning)
        self.setText("База данных или коллекция не обнаружены.\n\nCоздать новую базу данных(ОК) "
                     "или закрыть приложение(close)?")
        self.setWindowTitle("Соединение с БД")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)

