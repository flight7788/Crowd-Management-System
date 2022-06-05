from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryAllStu(MessageProcessor):
        
    def execute(self,params=[]):
            
        result = StudentProfile().get_students()
        
        if not result['is_success'] :
            return self.return_fail_with_reason(result['message'])
        
        sorted_key = sorted([int(x) for x in result['data'].keys()])
        result_list = list()
        for key in sorted_key:
            result_list.append(result['data'][str(key)])
        
        if result['is_success'] and len(result_list)>0 :
            return self.return_success_with_data(result_list)
   

        