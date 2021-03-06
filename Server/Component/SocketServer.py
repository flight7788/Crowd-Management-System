from threading import Thread
import socket
import json
import copy
from Component.Logger import Logger

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
            Logger().info("Server Message # : {} Connected".format(address))
            print("Server Message # : {} Connected".format(address))
            
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
                message = connection.recv(20000000).strip().decode()
            except Exception as e:
                keep_going = False
                rtn_msg = dict()
                rtn_msg['status'] = 'Fail'
                rtn_msg['reason'] = 'Fatal Error: Transmission Error : {}'.format(e)
                Logger().error('Fatal Error: Transmission Error : {}'.format(e))
                       
                connection.send("Error".encode())
            else:
                if not message:
                    break
                
                #print(message)
                try:
                  message = json.loads(message)
                except Exception as e:
                     rtn_msg['status'] = 'Fail'
                     rtn_msg['reason'] = 'Fatal Error: JSON not a valid format : {}'.format(e)
                     Logger().error('Fatal Error: JSON not a valid format : {}'.format(e))
                     connection.send("Error".encode())
                     
                
                if message['command'] == "close":
                    connection.send("closing".encode())
                    break
                else:
                    
                    show_dict =  copy.deepcopy(message)
                    
                    if show_dict['command'] in ['swipe_card','manual_check'] :
                       print(len(show_dict['parameters']['img']))
                       show_dict['parameters']['img'] = 'list (uint8)'
                       
                    print('Server Receive # : {} from {}'.format(show_dict,address))
                    Logger().info('Server Receive # : {} from {}'.format(show_dict,address))
                    
                    
                    print(type(message['parameters']))
                    print(len(message['parameters']))
                    if(type(message['parameters'])  is str ):
                      message['parameters']=dict()
                    message['parameters']['client_IP'] = address[0]
                    reply_msg = self.handler(message)
                    connection.send(json.dumps(reply_msg).encode())
                    
        
        connection.close()
        print("Server Message # : {} Disconnected".format(address))
        Logger().info("Server Message # : {} Disconnected".format(address))
        

        
