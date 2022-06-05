from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
class ModifyStu:
        
    def execute(self,params=[]):
    
        if ('student_id' in params  and 'student_name' in params and 'card_no' in params):
            student_id = params['student_id']
            student_name = params['student_name']
            card_no = params['card_no']
            
            student_profile = StudentProfile().get_a_student_by_student_id(student_id = student_id)
            if not student_profile['is_success'] :
                 return {'status' : 'Fail' , 'reason' : 'Student id {} is not exists'.format(student_id)}
             
            # card_no_profile = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            # if card_no_profile['is_success'] :
            #      return {'status' : 'Fail' , 'reason' : 'Card No {} alreay exists'.format(card_no)}
              
     
            profile_id = student_profile['data']['id']
            update_student = StudentProfile().update_a_student(id = profile_id, student_name=student_name,card_no=card_no)
            
            #check if card_no exists
            if not update_student['is_success'] :
                return {'status' : 'Fail' , 'reason' : update_student['message'] }

    
            return  {'status':'Success' }
        
        return {'status' : 'Fail' , 'reason' : 'student_id , student_name , card_no is required'}

