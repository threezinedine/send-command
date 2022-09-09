from cores import MySocket


if __name__ == "__main__":
    socket = MySocket("192.168.1.3", 1234)
    socket.send("30 30 26")
    socket.close()
