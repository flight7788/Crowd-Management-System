from threading import Thread
from queue import Queue
import socket
import json

class SocketServer(Thread):
    def __init__(self, host, port , handler):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.handler = handler

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection,
                                address=address)


    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except:
                keep_going = False
            else:
                if not message:
                    break
                message = json.loads(message)
                if message['command'] == "close":
                    connection.send("closing".encode())
                    break
                else:
                    print("server received: {} from {}".format(message,address))
                    reply_msg = self.handler(message)
                    
                    connection.send(json.dumps(reply_msg).encode())
                    
        
        connection.close()
        print("close connection")
        

        
