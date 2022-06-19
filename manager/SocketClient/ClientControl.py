from SocketClient.SocketClient import SocketClient
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import json

IP = "140.124.39.131"
PORT = 28888

class ClientControl:
    def __init__(self):
        self.client_socket = SocketClient(IP,PORT)

    def sent_command(self, command, parameters):
        self.client_socket.send_command(command,parameters)
        result = self.client_socket.wait_response()
        return result

class ExecuteCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, command,data):
        super().__init__()
        self.command = command
        self.data = data

    def run(self):
        result = ClientControl().sent_command(self.command,self.data)
        self.return_sig.emit(json.dumps(result))
        