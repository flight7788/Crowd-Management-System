from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from datetime import datetime
from Component.MessageProcessor import MessageProcessor
from Component.ImageProcessor import ImageProcessor

class Swipe(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('card_no' in params  and 'time' in params):
            card_no = params['card_no']
            time = params['time']
            img_binary =  params['img_binary'] if ('img_binary' in params)  else  ''
            student_profile = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            
            
            #check datetime format is valid
            try:
                datetime.strptime(time,'%Y/%m/%d %H:%M:%S')
            except ValueError as e:
                self.return_fail_with_reason('Datetime format must like [YYYY/mm/dd HH:MM:SS], detail: {}'.format(e))
            
            #check if card_no exists
            if not student_profile['is_success'] :
                self.return_fail_with_reason('card_no is not found')

            student_name = student_profile['data']['student_name']
            student_id = student_profile['data']['student_id']
            swipe_logs = StudentLog().get_logs_by_card_no(card_no)
            swipe_status = self.getSwipeStatus(swipe_logs)
            
            img_file  =  ImageProcessor().decodeImg(img_binary)
            
            result = StudentLog().add_log(card_no, img_file,'',swipe_status,time) 
            
            if not result['is_success'] :
                 return self.return_fail_with_reason(result['message'])
            
            return self.return_success_with_data({'student_name' : student_name ,'status' : swipe_status ,'student_id': student_id})
     
        return self.return_fail_with_reason('card_no and time is required')


        
    
    def getSwipeStatus(self,swipe_log):
    
        #if no data, means first swipe in
        if(swipe_log['is_success'] and len(swipe_log['data'])>0):   
                    
          #find last log in query result
          last_id = str(sorted([int(x) for x in swipe_log['data'].keys()])[-1])
          last_data = swipe_log['data'][last_id]
          
          if last_data['status'] == 'in' :
            return 'out'
          else:
            return 'in'
        
        else:
          return 'in'