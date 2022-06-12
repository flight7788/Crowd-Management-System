from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class CheckMember(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('card_no' in params):
            card_no = params['card_no']
            
            result = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            
            if(len(result)>0):
            
                return  self.return_success_with_data({'is_exist':True})
            else:
                return  self.return_success_with_data({'is_exist':False})
            
        return self.return_fail_with_reason('card_no is required')


        
    
    