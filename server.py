from cores import MyServer
from controllers import Controller
import socket


if __name__ == "__main__":
    server = MyServer(socket.gethostname(), 1234)
    server.run()
