from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor
class AddStu(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params  and 'name' in params and 'card_no' in params):
            id = params['id']
            name = params['name']
            card_no = params['card_no']
            
            student_id_profile = StudentProfile().get_a_student_by_student_id(id = id)
            if student_id_profile['is_success'] :
                return self.return_fail_with_reason('Student id {} alreay exists'.format(id))
             
            card_no_profile = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            if card_no_profile['is_success'] :
                 return self.return_fail_with_reason('Card No {} alreay exists'.format(card_no))
            
            
            add_student = StudentProfile().add_student(name = name,card_no = card_no,id = id)
            
            #check if card_no exists
            if not add_student['is_success'] :
                return self.return_fail_with_reason(add_student['message'])

            return  self.return_success()
        
        return self.return_fail_with_reason('card_no , time and status is required')

