from FireStore.FireStoreConnector import FireStoreInitializer
from SocketServer import SocketServer
from Service.QueryStuService import QueryStu
from Service.QueryCardService import QueryCard
from Service.SwipeService import Swipe

FIRESTORE_KEYCHAIN = "connection_info.json"
HOST = "140.124.39.131"
PORT = 28888


FUNCTION_METHOD = {
      'query_stu' : QueryStu,
      'query_card' :  QueryCard,
      'swipe' : Swipe,
    # 'delete' : DelStu,
    # 'modify' : ModifyStu,
}

def receive_handler(messages):
    cmd = messages['command']
    params = messages['parameter']
    
    print(messages)
    
    try:
        return FUNCTION_METHOD[cmd]().execute(params)
    
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



    #StudentLog(db).add_log('100000','','0','in','2022/01/01')
    #print(StudentLog(db).get_a_log(2))
    #StudentProfile(db).add_student('何翊宇','100000')
    #print(StudentProfile(db).get_students())
    #print(db.insert(collection_name='student_profile',data={'name':'123','stu':'heyiyu'}))
    #print(db.update(collection_name='student_profile',id=4,data={'name':'111','stu':'111111'}))
    #print(db.delete(collection_name='student_profile',id=4))
    #print(db.query(collection_name='student_profile',column_name = 'name', key_word='111'))
    #print(db.query(collection_name='student_profile',id=1))