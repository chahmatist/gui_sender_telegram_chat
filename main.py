import sys

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QApplication

from telega import Telega
from window import *


class MainWindow(QMainWindow):  # главное окно
    def __init__(self, parent=None):
        """ init QT window """
        QWidget.__init__(self, parent)
        self.settings = QSettings('MainWindow', 'myApp')


        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        token = self.settings.value("token")
        chat_id = self.settings.value("chat_id")
        signed = self.settings.value("signed")

        if token:
            self.ui.lineEdit_token.setText(token)
        if chat_id:
            self.ui.lineEdit_chat_id.setText(chat_id)
        if signed:
            self.ui.plainTextEdit_signed.setPlainText(signed)

        # buttons signals
        self.ui.button_get_chat_id.clicked.connect(self.click_get_chat_id)
        self.ui.button_send_message.clicked.connect(self.click_send_message)

    def closeEvent(self, e):
            # Write window size and position to config file
            self.settings.setValue("token", self.ui.lineEdit_token.text())
            self.settings.setValue("chat_id", self.ui.lineEdit_chat_id.text())
            self.settings.setValue("signed", self.ui.plainTextEdit_signed.toPlainText())
            e.accept()

    @staticmethod
    def __warning_message(title: str, text: str):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def click_get_chat_id(self):
        token = self.ui.lineEdit_token.text()
        if token:
            telega = Telega(token)
            data = telega.get_chat_id()
            print(data)
            if data['ok'] and len(data['result']) > 1:

                chat_id = data['result'][0]['my_chat_member']['chat']['id']
                self.ui.lineEdit_chat_id.setText(str(chat_id))
            else:
                self.__warning_message(str(data['error_code']), str(data['description']))

        else:
            self.__warning_message('test', "не введен токен")

    def click_send_message(self):
        signed = self.ui.plainTextEdit_signed.toPlainText()
        message = self.ui.textEdit_message.toPlainText()
        text = str(message) + '\n' + str(signed)
        print(text)
        token = self.__check_token()
        chat_id = self.__check_chat_id()
        if token and chat_id:
            telega = Telega(token)
            telega.send_message(token, chat_id, text)

# todo: добавить проверку токена [0-9]{9}:[a-zA-Z0-9_-]{35}
    def __check_token(self):
        token = self.ui.lineEdit_token.text()
        if token:
            return token
        else:
            # [0-9]{9}:[a-zA-Z0-9_-]{35}
            self.__warning_message('Ошибка', "не введен токен")
            return None

    def __check_chat_id(self):
        chat_id = self.ui.lineEdit_chat_id.text()
        if chat_id:
            return chat_id
        else:
            self.__warning_message('Ошибка', "не введен чат ид")
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
