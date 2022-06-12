from tkinter import SW
from Component.FireStore.FireStoreConnector import FireStoreInitializer
from Component.SocketServer import SocketServer
from Component.MessageProcessor import MessageProcessor
from Component.Logger import Logger
from Service.QueryImgService import QueryImg
from Service.QueryStuLogsService import QueryStuLogs
from Service.CheckMemberService import CheckMember
from Service.SwipeCardService import SwipeCard
from Service.ManualCtrlService import ManualCtrl
from Service.QueryStuProfileService import QueryStuProfile
from Service.AddStuService import AddStu
from Service.DeleteStuService import DeleteStu
from Service.ModifyStuService import ModifyStu
from Service.QueryAllStuService import QueryAllStu
from Service.QueryLogsByTimeService import QueryLogsByTime
from Service.QueryImgService import QueryImg
from Component.Database.DBConnection import DBConnection


FIRESTORE_KEYCHAIN = "connection_info.json"
HOST = "140.124.39.131"
PORT = 28888


FUNCTION_METHOD = {
      'query_stu_logs' : QueryStuLogs,
      'check_member' :  CheckMember,
      'swipe_card' : SwipeCard,
      'manual_ctrl' : ManualCtrl,
      'query_stu_profile' : QueryStuProfile,
      'add_stu' : AddStu,
      'delete_stu' : DeleteStu,
      'modify_stu' : ModifyStu,
      'query_all_stu' : QueryAllStu,
      'query_logs_by_time' : QueryLogsByTime,
      'query_img' : QueryImg
}

def receive_handler(messages):
    
    cmd = messages['command'] if 'command' in messages else ''
    
    params = messages['parameters'] if 'parameters' in messages else {}
    params = messages['parameter'] if 'parameter' in messages else params

    if cmd not in FUNCTION_METHOD:
        return MessageProcessor().return_fail_with_reason('command:{} is not exists'.format(cmd))
    try:
        message = FUNCTION_METHOD[cmd]().execute(params)
        Logger().info('Server Response # : {}'.format(message))
        print('Server Response # : {}'.format(message))
        return message

    except  Exception as e:
        print('Exception occured : {}'.format(e))
        Logger().error('Exception occured : {}'.format(e))
        return MessageProcessor().return_fail_with_reason('Exception occured : {}'.format(e))

def main():
    
    #FireStoreInitializer(FIRESTORE_KEYCHAIN)
    
    DBConnection.db_file_path = "local.db"
    
    server = SocketServer(HOST, PORT , receive_handler)
    server.setDaemon=True
    server.serve()
    

    print('=============================================')
    print('Start Crownd Managemenmt System Server....')
    print('IP: {} , PORT: {}'.format(HOST,PORT))
    print('=============================================')
    print('Waiting for connection...')
    
    Logger().info('Server started at IP: {} , PORT: {}'.format(HOST,PORT))
    
    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")   
    Logger().info('Server closed'.format(HOST,PORT))

main()
