import sys
from views import MyWidget
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit
from cores import MySocket, MyServer
from models import Command
from models.properties import Property
from utils import convert_string_to_hex, convert_hex_to_string
from functools import partial


commands = {
    "" : {},
    "6" : {
            "name": "stop",
            "address": "6",
            "properties": [None, None, None, None, None, None]
        }, 
    "4": {
            "name": "run",
            "address": "4",
            "properties": [None, None, None, None, {'label':'Program', 'description': 'The program that the robot will run'}, None]
        },
    "5": {
            "name": "read encoder",
            "address": "5",
            "properties": [None, None, None, None, {'label': 'Channel', 'description': 'The output channel of the encoder'}, {'label': 'I/O port'}]
        }
}


class Controller:
    def __init__(self, socket_type=MySocket):
        self.app = QApplication(sys.argv)
        self.win = MyWidget(controller=self)
        self._socket_type = socket_type
        self.socket = None

        self.function_source = self.win.define_text_source('function_text')
        self.function_source.toggle_state(False)
        self.function_source.connect(self.update_param)

        self.function_property = Property(2, self.function_source)

    def update_param(self):
        if self.function_source.get_text() in commands.keys():
            self.update_param_with_valid_key()
        else:
            self.update_param_with_invalid_key()


    def update_param_with_invalid_key(self):
        paramBoxes = [self.win.define_text_source(f'param{index}_text') for index in range(1, 7)]
        paramLabels = [self.win.findChild(QLabel, f'param{index}_label') for index in range(1, 7)]
        self.win.reset_command()

        for paramBox, paramLabel in zip(paramBoxes, paramLabels):
            paramBox.reset()
            paramLabel.setText("")

    def update_param_with_valid_key(self):
        data = commands[self.function_source.get_text()]

        paramBoxes = [self.win.define_text_source(f'param{index}_text') for index in range(1, 7)]
        paramLabels = [self.win.findChild(QLabel, f'param{index}_label') for index in range(1, 7)]

        commandParams = [Property(4, paramBox) if prop is not None else None for prop, paramBox in zip(data["properties"], paramBoxes)]
        command = Command(data["name"], self.function_property, commandParams)

        for prop, paramLabel, paramBox in zip(data["properties"], paramLabels, paramBoxes):
            if prop is None:
                paramBox.reset()
                paramLabel.setText("")
            else:
                paramBox.toggle_state(False)
                paramLabel.setText(prop['label'])
                if 'description' in prop.keys():
                    paramLabel.setToolTip(prop['description'])

            def changeCommandLabel():
                self.win.findChild(QLabel, 'command').setText(command.get_command())

            paramBox.connect(changeCommandLabel)

        self.command = command.get_command()
        self.win.findChild(QLabel, 'command').setText(command.get_command())

    def show(self):
        self.win.show()
        try:
            sys.exit(self.app.exec_())
            self.socket.send(b'\xff')
        except:
            print("[EXITING] Client is existing...")

    def connect(self):
        try:
            ip, port = self.win.get_ip()
            self.socket = self._socket_type(ip, port)
        except Exception as e:
            print("[ERROR] Cannot connect to server...")
            self.win.set_error(e)

    def send(self, data):
        try: 
            self.socket.send(data)

            received_data = self.socket.recv()
            self.win.set_receive(convert_hex_to_string(received_data))
            print(f"[RECEIVE] Receive data {received_data}.")

            print(f"[SENT] Message \"{data}\"  is sent...")
        except Exception as e:
            print(f"[ERROR] {e}")
            self.win.set_error(str(e))
