from firebase_admin import firestore

class StudentProfile():  
    
    COLLECTION_NAME = 'student_profile'
    
    def __init__(self,commander = None): 
        self.commander = commander

    def get_students(self):
        return self.commander.query(self.COLLECTION_NAME)
        
    def get_a_student(self,id):   
        return self.commander.query(self.COLLECTION_NAME,id) 
        
    def add_student(self,student_name,card_no):
        return self.commander.insert(self.COLLECTION_NAME, {'student_name':student_name,'card_no': card_no}) 
        
    def del_student(self,id):
        return self.commander.delete(self.COLLECTION_NAME,id)
        