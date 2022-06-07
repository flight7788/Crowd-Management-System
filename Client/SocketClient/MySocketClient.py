import socket 
import json

BUFFER_SIZE = 20000

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))
 
    def send_command(self, command, parameters={}):
        send_data = {'command': command, "parameters": parameters}
        self.client_socket.send(json.dumps(send_data).encode()) 
        if command in ['swipe', 'manual_check']:
            send_data['parameters']['img_binary'] = 'list (uint8)'
        print('     The client sent data => ', send_data)

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print('     The client received data => ', raw_data)
        if raw_data == "closing":
            return False  
        return json.loads(raw_data)

if __name__ == '__main__':
    host = "140.124.39.131"
    port = 28888
    client = SocketClient(host, port)