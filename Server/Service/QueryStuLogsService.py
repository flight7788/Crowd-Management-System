from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryStuLogs(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('id' in params):
            id = params['id']
            
            result = StudentProfile().get_a_student_by_student_id(id=id)
            
            if not result['is_success'] :
                return self.return_fail_with_reason(result['message'])
            
            name = result['data']['name']
            card_no = result['data']['card_no']
            result = StudentLog().get_logs_by_card_no(card_no=card_no)
            sorted_key = sorted([int(x) for x in result['data'].keys()])
            result_list = list()
            
            for key in sorted_key:
                log = result['data'][str(key)]
                log['name'] = name
                result_list.append(log)

            if result['is_success'] and len(result_list)>0 :
                return self.return_success_with_data(result_list)
            
        return self.return_fail_with_reason(' id  is required')


        
    
    