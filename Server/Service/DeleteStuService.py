from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor
class DeleteStu(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params):
            id = params['id']
            
            student_profile = StudentProfile().get_a_student_by_student_id(id = id)
            if len(student_profile)==0 :
                 return self.return_fail_with_reason('Student id {} is not exists'.format(id))
    
            StudentProfile().del_student(id = id)
       
            return  self.return_success()
        
        return self.return_fail_with_reason('student_id is required')

