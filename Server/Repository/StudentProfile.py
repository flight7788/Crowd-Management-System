from FireStore.FireStoreCommander import FireStoreCommander

class StudentProfile():  
    
    COLLECTION_NAME = 'student_profile'
    
    def __init__(self): 
        
        self.commander = FireStoreCommander()

    def get_students(self):
        
        return self.commander.query(self.COLLECTION_NAME)
        
    def get_a_student(self,id):   
        
        return self.commander.query(self.COLLECTION_NAME,id) 
    
    def get_a_student_by_student_id(self,student_id):   
        
        query = self.commander.query(self.COLLECTION_NAME, column_name='student_id' ,key_word = student_id)
        
        if (query['is_success'] and len(query['data']) >0 ):
            data_id = next(iter(query['data']))
            first_data = query['data'][data_id]
            first_data['id'] = data_id
            return {'is_success' : True ,  'data' : first_data }
        
        return {'is_success' : False ,  'message' : 'not found'}
    
    def get_a_student_by_card_no(self,card_no):   
        
        query = self.commander.query(self.COLLECTION_NAME, column_name='card_no' ,key_word = card_no)
        
        if (query['is_success'] and len(query['data']) >0 ):
            data_id = next(iter(query['data']))
            first_data = query['data'][data_id]
            first_data['id'] = data_id
            return {'is_success' : True ,  'data' : first_data }
        
        return {'is_success' : False ,  'message' : 'not found'}
    
    def update_a_student(self, id , student_name='', card_no=''):
        
        data = {'student_name':student_name, 'card_no': card_no}
        
        return self.commander.update(self.COLLECTION_NAME,id,data) 
        
        
    def add_student(self,student_name='',card_no='',student_id=''):
        
        data = {'student_name':student_name,'card_no': card_no , 'student_id' : student_id}
        
        return self.commander.insert(self.COLLECTION_NAME, data) 
        
    def del_student(self,id):
        
        return self.commander.delete(self.COLLECTION_NAME,id)
        