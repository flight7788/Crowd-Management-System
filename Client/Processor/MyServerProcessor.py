from SocketClient.MySocketClient import SocketClient
from PyQt5 import QtCore

class ServerProcessor(QtCore.QThread):
    sendPassToServer_sig = QtCore.pyqtSignal(str, str, str)  
    sendManualPassToServer_sig = QtCore.pyqtSignal(str, str)  
    fail_sig = QtCore.pyqtSignal(str)

    def __init__(self, socketClient: SocketClient):
        super().__init__()
        self.socket_client = socketClient
        self.command = None
        self.parameter = None
        self.start_f = False

    def run(self):
        while self.start_f and self.socket_client != None:
            if self.command != None:
                recv_data = self.socket_client.wait_response()
                if self.command == 'swipe':
                    if recv_data['status'] == 'OK':
                        self.sendPassToServer_sig.emit(recv_data['data']['student_name'], 
                                                       recv_data['data']['student_id'], 
                                                       recv_data['data']['status'])
                    else:
                        print('Error swipe:{}'.format(recv_data['status']))
                        self.fail_sig.emit('sending fail')

                elif self.command == 'manual_check':
                    if recv_data['status'] == 'OK':
                        self.sendManualPassToServer_sig.emit(recv_data['data']['student_name'], 
                                                             self.parameter['status'])
                    else:
                        print('Error manual_check:{}'.format(recv_data['status']))
                        self.fail_sig.emit('not exist')
            self.command = None

    def start_waiting(self):
        if self.start_f == False:
            self.start_f = True
    
    def stop_waiting(self):
        if self.start_f == True:
            self.start_f = False

    def checkWithServer(self, card_no: str):
        self.socket_client.send_command('query_card', {'card_no':card_no})
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] == 'OK':   
            return recv_data['data']['is_school_member']
        else:
            print('Error query_card:{}'.format(recv_data['status']))
        return False
        
    def sendPassToServer(self, card_no: str, time: str, imgEncode=''):
        self.parameter = {  'card_no': card_no, 
                            'time': time,  
                            'img_binary': imgEncode}
        self.socket_client.send_command('swipe', self.parameter)
        self.command = 'swipe'  
        
    def sendManualPassToServer(self, student_id: str, time: str, imgEncode='', status=''):
        self.parameter = {  'student_id': student_id, 
                            'time': time,  
                            'img_binary': imgEncode, 
                            'status': status}
        self.socket_client.send_command('manual_check', self.parameter)    
        self.command = 'manual_check'
        

    