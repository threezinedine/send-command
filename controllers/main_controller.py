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
    "5": {
            "name": "run",
            "address": "5",
            "properties": [None, None, None, None, {'label':'Program', 'description': 'The program that the robot will run'}, None]
        },
    "4": {
            "name": "reset",
            "address": "4",
            "properties": [None, None, None, None, None, None]
        },
    "12": {
            "name": "control output",
            "address": "12",
            "properties": [{'label': 'IO out put', 'reverse': True}, {'label': 'Status', 'reverse': True}, None, None, None, None]
        },
    "14": {
        "name": "read encoder",
        "address": "14",
        "properties": [None, None, None, None, {'label': 'IO out put'}, {'label': 'Encoder'}]
        },
    "1": {
        "name": "move",
        "address": "1",
        "properties": [
            {"label": 'X'},
            {'label': 'Y'},
            {'label': 'Z'},
            {'label': 'Angle'},
            {'label': 'Encoder'},
            {'label': 'Run'}
            ]
        },
    "3": {
        "name": "move directly",
        "address": "3",
        "properties": [
            {"label": 'X', 'reverse': True},
            {'label': 'Y', 'reverse': True},
            {'label': 'Z', 'reverse': True},
            {'label': 'Angle', 'reverse': True},
            {'label': 'Speed', 'reverse': True},
            None
            ]
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

        self.function_property = Property(2, self.function_source, is_reverse=False)
        self.command = None

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

        commandParams = [Property(4, paramBox, is_reverse=True if 'reverse' in prop.keys() else False) if prop is not None else None for prop, paramBox in zip(data["properties"], paramBoxes)]
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

            self.command = command.get_command()
            def changeCommandLabel():
                self.win.findChild(QLabel, 'command').setText(command.get_command())
                self.command = command.get_command()

            paramBox.connect(changeCommandLabel)

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
            self.win.set_error(str(e))

    def send(self, data):
        try: 
            print(convert_string_to_hex(data))
            self.socket.send(data)

            received_data = self.socket.recv()
            self.win.set_receive(convert_hex_to_string(received_data))
            print(f"[RECEIVE] Receive data {received_data}.")

            print(f"[SENT] Message \"{data}\"  is sent...")
        except Exception as e:
            print(f"[ERROR] {e}")
            self.win.set_error(str(e))

    def disconnect(self):
        print("Exit")
        self.socket.close()


