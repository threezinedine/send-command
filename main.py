import sys
from controllers import Controller
from cores import MySocket, MyServer



def main():
    controller = Controller(MySocket)
    controller.show()


if __name__ == "__main__":
    main()
