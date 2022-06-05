from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
class QueryStuProfile:
        
    def execute(self,params=[]):
        
        if ('student_id' in params):
            student_id = params['student_id']
            
            result = StudentProfile().get_a_student_by_student_id(student_id=student_id)
            
            if not result['is_success'] :
                return {'status' : 'Fail' , 'reason' : result['message'] }
            
            if result['is_success'] and len(result['data'])>0 :
                return  {'status':'Success' , 'data':result['data'] }
            
        return {'status' : 'Fail' , 'reason' : 'student_id  is required'}

        
    
    