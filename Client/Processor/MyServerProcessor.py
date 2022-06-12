from SocketClient.MySocketClient import SocketClient

class ServerProcessor():
    def __init__(self, socketClient: SocketClient):
        self.socket_client = socketClient

    def checkCardWithServer(self, card_no: str):
        self.socket_client.send_command('check_member', {'card_no':card_no})
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] == 'OK':   
            return recv_data['data']['is_exist']
        else:
            print('Error check_member:{}'.format(recv_data['status']))
        return False
    
    def sendPassToServer(self, card_no='', time='', imgEncode=''):
        self.socket_client.send_command('swipe_card', {  'card_no': card_no, 
                                                         'time': time,  
                                                         'img': imgEncode})
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('swipe_card:{}'.format(recv_data['status']))
            return False
        return recv_data['data']

    def sendManualPassToServer(self, student_id='', time='', imgEncode='', status=''):
        self.socket_client.send_command('manual_ctrl', 
                    {   'id': student_id, 
                        'time': time,  
                        'img': imgEncode, 
                        'action': status})    
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('manual_ctrl:{}'.format(recv_data['status']))
            return False
        return recv_data['data']['name']
    
    def checkStuWithServer(self, student_id: str):
        self.socket_client.send_command('query_stu_logs', { 'id': student_id })    
        recv_data = self.socket_client.wait_response()
        if recv_data['status'] != 'OK':
            print('query_stu_logs:{}'.format(recv_data['status']))
            return False
        return recv_data['data']