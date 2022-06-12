from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class ModifyStu(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params  and 'name' in params and 'card_no' in params):
            id = params['id']
            name = params['name']
            card_no = params['card_no']
            
            student_profile = StudentProfile().get_a_student_by_student_id(id = id)
            if len(student_profile)==0 :
                 return self.return_fail_with_reason('ID {} is not exists'.format(id))
             
     
            StudentProfile().update_a_student(id = id, name=name,card_no=card_no)
            
            return self.return_success()
        
        return self.return_fail_with_reason('id , name , card_no is required')


