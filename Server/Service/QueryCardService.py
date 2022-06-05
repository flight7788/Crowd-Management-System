from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
class QueryCard:
        
    def execute(self,params=[]):
        
        if ('card_no' in params):
            card_no = params['card_no']
            
            result = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            
            if not result['is_success'] :
                return {'status' : 'Fail'}

            return  {'status':'Success' , 'data': {'is_school_member':True} }
            
        return {'status' : 'Fail' , 'reason' : 'card_no is required'} 

        
    
    