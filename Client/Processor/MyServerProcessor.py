from SocketClient.MySocketClient import SocketClient

class ServerProcessor:
    def __init__(self, socketClient: SocketClient):
        self.socket_client = socketClient

    def checkWithServer(self, card_no):
        self.socket_client.send_command('query_card', {'card_no':card_no})
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('query_card:{}'.format(recv_data['status']))
            return False
        return recv_data['data']['is_school_member']
        
    def sendPassToServer(self, card_no='', time='', imgEncode=''):
        self.socket_client.send_command('swipe', {  'card_no': card_no, \
                                                    'time': time,  \
                                                    'img_binary': imgEncode})
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('swipe:{}'.format(recv_data['status']))
            return False
        return recv_data['data']

    def sendManualPassToServer(self, student_id='', time='', imgEncode='', status=''):
        self.socket_client.send_command('manual_check', \
                    {   'student_id': student_id, \
                        'time': time,  \
                        'img_binary': imgEncode, \
                        'status': status})    
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('manual_check:{}'.format(recv_data['status']))
            return False
        return recv_data['data']['student_name']
    