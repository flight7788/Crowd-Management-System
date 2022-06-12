from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from datetime import datetime
from Component.MessageProcessor import MessageProcessor
from Component.ImageProcessor import ImageProcessor

class SwipeCard(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('card_no' in params  and 'time' in params):
            
            card_no = params['card_no']
            time = params['time']
            client_ip = params['client_IP']
            img_binary =  params['img'] if ('img' in params)  else  ''
            
            student_profile = StudentProfile().get_a_student_by_card_no(card_no = card_no)
            
            #check datetime format is valid
            try:
                datetime.strptime(time,'%Y/%m/%d %H:%M:%S')
            except ValueError as e:
                return self.return_fail_with_reason('Datetime format must like [YYYY/mm/dd HH:MM:SS], detail: {}'.format(e))
            
            #check if card_no exists
            if len(student_profile)==0 :
                return self.return_fail_with_reason('card_no is not found')
            name = student_profile[0]['name']
            id = student_profile[0]['id']
            action = self.getLastSwipeAction(id)
            
            img_file  =  ImageProcessor().decodeImg(img_binary)
            
    
            StudentLog().add_log(card_no, img_file, client_ip,action,time) 
            
            
            return self.return_success_with_data({'name' : name ,'action' : action ,'id': id})
     
        return self.return_fail_with_reason('card_no and time is required')


        
    
    def getLastSwipeAction(self,id):
    
        swipe_log = StudentLog().get_last_log_by_stu_id(id=id)
        #if no data, means first swipe in
        if(len(swipe_log)>0):   
                    
          if swipe_log[0]['action'] == 'in' :
            return 'out'
          else:
            return 'in'
        
        else:
          return 'in'