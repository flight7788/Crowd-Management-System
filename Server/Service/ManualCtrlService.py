from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from datetime import datetime
from Component.MessageProcessor import MessageProcessor
from Component.ImageProcessor import ImageProcessor  

class ManualCtrl(MessageProcessor):
        
    def execute(self,params=[]):
    
        if ('id' in params  and 'time' in params and 'action' in params):
            id = params['id']
            time = params['time']
            action = params['action']
            img =  params['img'] if ('img' in params)  else  ''
            
            #check datetime format is valid
            try:
                datetime.strptime(time,'%Y/%m/%d %H:%M:%S')
            except ValueError as e:
                return self.return_fail_with_reason('Datetime format must like [YYYY/mm/dd HH:MM:SS], detail: {}'.format(e))
                
            student_profile = StudentProfile().get_a_student_by_student_id(id = id)
            
            #check if card_no exists
            if len(student_profile)==0 :
                return self.return_fail_with_reason('student_id is not found')
            
            card_no = student_profile[0]['card_no']
            name = student_profile[0]['name']

            img_file  =  ImageProcessor().decodeImg(img)
            
            StudentLog().add_log(card_no,img_file,'', action ,time) 
            
            return  self.return_success_with_data({'name' : name})
        
        return self.return_fail_with_reason('card_no , time and action is required')

