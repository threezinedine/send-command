import socket
from utils import convert_string_to_hex


class MySocket:
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        print(f"[CONNECTED]: Connect to {host}:{port}")

    def send(self, data):
        self._socket.send(convert_string_to_hex(data))

    def recv(self):
        return self._socket.recv(1000)

    def close(self):
        self._socket.close()


class MyServer:
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._socket.listen(3)

    def run(self):
        print("[RUNNING] Server is starting ...")

        connection, addr = self._socket.accept()
        print(f"[CONNECTED] {addr[0]}:{addr[1]} connected to server")
        while True:
            data = connection.recv(1000)
            if data == b'\xff':
                print("[EXISTING] Server is stopping...")
                break

            if data == b'\xaa':
                response = convert_string_to_hex("30 30 30 08 50 80")
                connection.sendall(response)
                print(f"[SENT] Sent {response} to {addr[0]}:{addr[1]}")

            print(data)
