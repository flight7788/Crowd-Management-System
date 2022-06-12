from Repository.StudentLog import StudentLog
from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor
from Component.ImageProcessor import ImageProcessor
from os.path import exists

class QueryImg(MessageProcessor):
        
    def execute(self,params=[]):
        
        if ('file_name' in params):
            filename = params['file_name']
            if(exists(filename)):
                img_list = ImageProcessor().encodeImg(filename)

                if len(img_list)>0 :
                    return self.return_success_with_data(img_list)
                else:
                    return  self.return_fail_with_reason('Image is broken')
            else:
               return self.return_fail_with_not_found()
            
        return self.return_fail_with_reason('file_name is required')


        
    
    