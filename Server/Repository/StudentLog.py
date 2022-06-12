from Component.FireStore.FireStoreCommander import FireStoreCommander

class StudentLog():  
    
    COLLECTION_NAME = 'student_log'
    
    def __init__(self): 
        
        self.commander = FireStoreCommander()

    def get_logs(self):
        
        return self.commander.query(self.COLLECTION_NAME)
    
    def get_logs_by_card_no(self,card_no):
        
        return self.commander.query(self.COLLECTION_NAME,column_name='card_no',key_word = card_no)
        
    def get_a_log(self,id):   
        
        return self.commander.query(self.COLLECTION_NAME,id) 
        
    def add_log(self, card_no='' , img='' , client_IP='' , status=''  ,  time='' ):
        
        data = {'card_no':card_no,'img': img,'client_IP': client_IP ,'action':status , 'time': time}
        
        return self.commander.insert(self.COLLECTION_NAME, data) 
        
    def del_log(self,id):
        
        return self.commander.delete(self.COLLECTION_NAME,id)
        
        
