from datetime import datetime
from os.path import exists
class Logger:
    
    def __init__(self):
        time_stamp = datetime.now().strftime('%Y%m%d')
        self.path = './Logs/{}.log'.format(time_stamp)
        
        if(not(exists(self.path))):
            open(self.path, 'w').close()

    def log(self,type,msg):
        with open(self.path,'a+') as log:
            log.write('[{}] {} :{}\n'.format(type, datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'),msg))
             
    def info(self, msg=''):
        self.log('INFO',msg)
            
    def error(self, msg=''):
        self.log('ERROR',msg)
             
    def debug(self, msg=''):
        self.log('DEBUG',msg)

      