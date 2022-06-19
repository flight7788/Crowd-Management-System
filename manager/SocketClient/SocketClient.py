import socket 
import json

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 20000000

class SocketClient:
    def __init__(self,host,port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))
 
    def send_command(self, command, parameters):
        self.command = command
        send_data = {'command': command,'parameters':parameters}
        print("The client sent data => {}".format(send_data))
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        received_data = self.client_socket.recv(BUFFER_SIZE).decode()
        received_data = json.loads(received_data)
        if self.command == "query_img":
            if received_data['status'] == "OK":
                print("The client received data => {}".format({'status': 'OK', 'data': {'img': 'unit_8'}}))
            else:
                print("The client received data => {}".format(received_data))
        else :
            print("The client received data => {}".format(received_data))
        return received_data