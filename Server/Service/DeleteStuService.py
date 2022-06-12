from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor
class DeleteStu(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params):
            id = params['id']
            
            student_profile = StudentProfile().get_a_student_by_student_id(id = id)
            if not student_profile['is_success'] :
                 return self.return_fail_with_reason('Student id {} is not exists'.format(id))
     
            profile_id = student_profile['data']['id']
            remove_student = StudentProfile().del_student(id = profile_id)
            
            #check if card_no exists
            if not remove_student['is_success'] :
                return self.return_fail_with_reason(remove_student['message'])

    
            return  self.return_success()
        
        return self.return_fail_with_reason('student_id is required')

