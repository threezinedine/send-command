import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from functools import partial
from .i_text_source import TextSource


UI_DIR = "ui"


class MyWidget(QWidget):
    def __init__(self, ui_dir="main.ui", controller=None):
        QWidget.__init__(self)
        self.initUI(ui_dir)
        self.controller = controller

        self.connect_btn = self.findChild(QPushButton, 'connectBtn')
        self.connect_btn.clicked.connect(partial(self.controller.connect))
        self.msgBox = self.findChild(QLineEdit, 'sentMsg')

    def define_text_source(self, name):
        child = self.findChild(QLineEdit, name)
        text_source = TextSource(child)
        return text_source

    def set_controller(self, controller):
        self.controller = controller

    def initUI(self, ui_dir):
        loadUi(os.path.join(UI_DIR, ui_dir), self)

    def get_ip(self):
        ip_pack = '.'.join([self.findChild(QLineEdit, f'ip_{index}').text() for index in range(1, 5)])
        port = self.findChild(QLineEdit, 'port').text()

        return ip_pack, int(port)

    def set_receive(self, data):
        self.findChild(QLineEdit, 'receivedMsg').setText(data)

    def set_error(self, msg):
        self.findChild(QLabel, 'errorMsg').setText(msg)

    def reset_command(self):
        self.findChild(QLabel, 'command').setText("")
