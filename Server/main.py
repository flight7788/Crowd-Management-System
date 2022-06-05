from FireStore.FireStoreConnector import FireStoreInitializer
from SocketServer import SocketServer
from Service.QueryStuService import QueryStu
from Service.QueryCardService import QueryCard
from Service.SwipeService import Swipe
from Service.ManualCheckService import ManualCheck
from Service.QueryStuProfileService import QueryStuProfile
from Service.AddStuService import AddStu
from Service.DeleteStuService import DeleteStu
from Service.ModifyStuService import ModifyStu
from Service.QueryAllStuService import QueryAllStu
from Service.QueryLogsService import QueryLogs

FIRESTORE_KEYCHAIN = "connection_info.json"
HOST = "140.124.39.131"
PORT = 28888


FUNCTION_METHOD = {
      'query_stu' : QueryStu,
      'query_card' :  QueryCard,
      'swipe' : Swipe,
      'manual_check' : ManualCheck,
      'query_stu_profile' : QueryStuProfile,
      'add_stu' : AddStu,
      'delete_stu' : DeleteStu,
      'modify_stu' : ModifyStu,
      'query_all_stu' : QueryAllStu,
      'query_logs' : QueryLogs
}

def receive_handler(messages):
    cmd = messages['command']
    params = messages['parameter']
    
    try:
        
        message = FUNCTION_METHOD[cmd]().execute(params)
        print('Server Response # : {}'.format(message))
        return message
    
    except  Exception as e:

        print('{}'.format(e))
        return {'status':'FAIL','data' : '{}'.format(e)}

def main():
    
    FireStoreInitializer(FIRESTORE_KEYCHAIN)
    server = SocketServer(HOST, PORT , receive_handler)
    server.setDaemon=True
    server.serve()
    
    print('=============================================')
    print('Start Crownd Managemenmt System Server....')
    print('IP: {} , PORT: {}'.format(HOST,PORT))
    print('=============================================')
    print('Waiting for connection...')
    
    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")   

main()
