from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class ModifyStu(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params  and 'name' in params and 'card_no' in params):
            id = params['id']
            name = params['name']
            card_no = params['card_no']
            
            student_profile = StudentProfile().get_a_student_by_student_id(id = id)
            if not student_profile['is_success'] :
                 return self.return_fail_with_reason('ID {} is not exists'.format(id))
             
            # card_no_profile = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            # if card_no_profile['is_success'] :
            #      return {'status' : 'Fail' , 'reason' : 'Card No {} alreay exists'.format(card_no)}
              
     
            profile_id = student_profile['data']['id']
            update_student = StudentProfile().update_a_student(id = profile_id, name=name,card_no=card_no)
            
            #check if card_no exists
            if not update_student['is_success'] :
                return self.return_fail_with_reason( update_student['message'])
    
            return self.return_success()
        
        return self.return_fail_with_reason('id , name , card_no is required')


