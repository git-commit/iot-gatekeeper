import threading
import socket

NODE_RED_SERVER_PORT = 4445
NODE_RED_CLIENT_PORT = 4444

class NodeRedDoorbellServerThread(threading.Thread):
    """
    Get doorbell triggers from NodeRed.
    """
    def __init__(self, intercom):
        super(NodeRedDoorbellServerThread, self).__init__()
        self.intercom = intercom

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self.running = True
            server_socket.bind(('', NODE_RED_SERVER_PORT))
            server_socket.listen(1)
            while self.running:
                conn, addr = server_socket.accept()
                with conn:
                    while self.running:
                        data = conn.recv(1024)
                        if not data:
                            print("no data breaking")
                            break
                        else:
                            self.intercom.onBellPressed()


class NodeRedDoorOpenClient():
    """
    Send open door commands to NodeRed.
    """
    def __init__(self):
        super(NodeRedDoorOpenClient, self).__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", NODE_RED_CLIENT_PORT))

    def sendOpenDoor(self):
        self.client_socket.send(b'open')
