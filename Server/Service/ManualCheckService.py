from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from datetime import datetime

class ManualCheck:
        
    def execute(self,params=[]):
    
        if ('student_id' in params  and 'time' in params and 'status' in params):
            student_id = params['student_id']
            time = params['time']
            status = params['status']
            img_binary =  params['img_binary'] if ('img_binary' in params)  else  ''
            
            #check datetime format is valid
            try:
                datetime.strptime(time,'%Y/%m/%d %H:%M:%S')
            except ValueError as e:
                return  {'status':'Fail' , 'reason': 'Datetime format must like [YYYY/mm/dd HH:MM:SS], detail: {}'.format(e)  }
                
            
            
            
            student_profile = StudentProfile().get_a_student_by_student_id(student_id = student_id)
            
            #check if card_no exists
            if not student_profile['is_success'] :
                return {'status' : 'Fail' , 'reason' : 'student_id is not found'}

            student_name = student_profile['data']['student_name']
            card_no = student_profile['data']['card_no']

            result = StudentLog().add_log(card_no,img_binary,'', status ,time) 
            
            if not result['is_success'] :
                return {'status' : 'Fail' ,'reason' : result['message'] }
            
            return  {'status':'Success' , 'data': {'student_name' : student_name} }
        
        return {'status' : 'Fail' , 'reason' : 'card_no , time and status is required'}
