from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryStuProfile(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('student_id' in params):
            student_id = params['student_id']
            
            result = StudentProfile().get_a_student_by_student_id(student_id=student_id)
            
            if not result['is_success'] :
                return self.return_fail_with_reason(result['message'])
            
            if result['is_success'] and len(result['data'])>0 :
                return self.return_success_with_data(result['data'])
            
        return self.return_fail_with_reason('student_id  is required')


        
    
    