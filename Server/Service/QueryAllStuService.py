from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryAllStu(MessageProcessor):
        
    def execute(self,params=[]):
            
        result = StudentProfile().get_students()
        
        if not result['is_success'] :
            return self.return_fail_with_reason(result['message'])
        
        if result['is_success'] and len(result['data'])>0 :
            return self.return_success_with_data(result['data'])
   

        
    
    