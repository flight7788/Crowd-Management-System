from Repository.StudentLog import StudentLog
from datetime import datetime
from Component.MessageProcessor import MessageProcessor

class QueryLogs(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('start_time' in params and 'end_time' in params):
            start_time = params['start_time']
            end_time  = params['end_time']
            
            try:
                start_time = datetime.strptime(start_time,'%Y/%m/%d %H:%M:%S')
                end_time = datetime.strptime(end_time,'%Y/%m/%d %H:%M:%S')
            except ValueError as e:
                return self.return_fail_with_reason('Datetime format must like [YYYY/mm/dd HH:MM:SS], detail: {}'.format(e))
                
            result = StudentLog().get_logs()
            logs = result['data']   
            filter_data = dict()
            
            for key, value in logs.items():
                try:
                    print(value['swipe_time'])
                    swipe_time = datetime.strptime(value['swipe_time'],'%Y/%m/%d %H:%M:%S')
                    if swipe_time>= start_time and swipe_time <= end_time :
                        filter_data[key] = value
                    
                except Exception as e:
                    print('Ignore : Parse SwipeDateTime Error, {} , date id is {}'.format(e,key))
                    pass
            
            if result['is_success'] and len(logs)>0 :
                return self.return_success_with_data(filter_data)
            
            else :
                self.return_fail_with_reason('no data')
            
        return self.return_fail_with_reason('start_time and end_time is required')


        
    
    