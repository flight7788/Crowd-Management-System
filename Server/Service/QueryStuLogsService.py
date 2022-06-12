from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryStuLogs(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('id' in params):
            id = params['id']
            
            result = StudentProfile().get_a_student_by_student_id(id=id)
            
            if len(result) ==0:
                return self.return_fail_with_reason('student id not found')
            
            card_no = result[0]['card_no']
            result = StudentLog().get_logs_by_card_no(card_no=card_no)
        

            if len(result)>0 :
                return self.return_success_with_data(result)
            else:
                return self.return_fail_with_not_found()
            
        return self.return_fail_with_reason(' id  is required')


        
    
    