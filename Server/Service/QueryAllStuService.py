from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
class QueryAllStu:
        
    def execute(self,params=[]):
            
        result = StudentProfile().get_students()
        
        if not result['is_success'] :
            return {'status' : 'Fail' ,  'reason' : result['message'] }
        
        if result['is_success'] and len(result['data'])>0 :
            return  {'status':'Success' , 'data':result['data'] }
   

        
    
    