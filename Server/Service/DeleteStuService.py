from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
class DeleteStu:
        
    def execute(self,params=[]):
    
        if ('student_id' in params):
            student_id = params['student_id']
            
            student_profile = StudentProfile().get_a_student_by_student_id(student_id = student_id)
            if not student_profile['is_success'] :
                 return {'status' : 'Fail' , 'reason' : 'Student id {} is not exists'.format(student_id)}
     
            profile_id = student_profile['data']['id']
            remove_student = StudentProfile().del_student(id = profile_id)
            
            #check if card_no exists
            if not remove_student['is_success'] :
                return {'status' : 'Fail' , 'reason' : remove_student['message'] }

    
            return  {'status':'Success' }
        
        return {'status' : 'Fail' , 'reason' : 'student_id is required'}

