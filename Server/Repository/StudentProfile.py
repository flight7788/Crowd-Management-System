from Component.Database.DBCommander import DBCommander

class StudentProfile(DBCommander):  
    

    def get_students(self):
        
        command = "SELECT * from profile ;"
        
        return self.query_data(command)
        
    
    def get_a_student_by_student_id(self,id):   
        
        command = "SELECT * from profile where id = '{}' ;".format(id)
        
        return self.query_data(command)
    
    def get_a_student_by_card_no(self,card_no):   
        
        command = "SELECT * from profile where card_no = '{}' ;".format(card_no)
        
        return self.query_data(command)
    
    def update_a_student(self, id , name='', card_no=''):
        
        
        command = "update profile set name = '{}' , card_no = '{}' where id = '{}' ;".format(name,card_no,id)
        
        return self.execute(command)
        
        
    def add_student(self,name='',card_no='',id=''):
        
        command = "INSERT INTO profile (name,id,card_no) VALUES  ('{}','{}','{}');".format(name,id,card_no)
        
        return self.execute(command)
        
    def del_student(self,id):
        
        command = "delete from profile where id = '{}' ;".format(id)
        
        return self.execute(command)
        
