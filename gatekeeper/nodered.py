import threading

NODE_RED_SERVER_PORT = 4445
NODE_RED_CLIENT_PORT = 4444

class NodeRedDoorbellServerThread(threading.Thread):
    """
    Get doorbell triggers from NodeRed.
    """
    def __init__(self, intercom):
        super(NodeRedServerThread, self).__init__()
        self.intercom = intercom
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        

    def run(self):
        self.server_socket.bind(("", NODE_RED_SERVER_PORT))
        self.server_socket.listen(1)
        conn, addr = self.server_socket.accept()
        while running:
            data = conn.recv(1024)
            if not data:
                print("no data breaking")
                break
            else:
                intercom.onBellPressed()
        conn.close()


class NodeRedDoorOpenClient():
    """
    Send open door commands to NodeRed.
    """
    def __init__(self):
        super(NodeRedClientThread, self).__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect("127.0.0.1", NODE_RED_CLIENT_PORT)

    def sendOpenDoor(self):
        self.client_socket.send(1)
