from Repository.StudentProfile import StudentProfile
from Component.MessageProcessor import MessageProcessor

class QueryAllStu(MessageProcessor):
        
    def execute(self,params=[]):
        
        data = StudentProfile().get_students()
        
        if(len(data)>0):
              return self.return_success_with_data(StudentProfile().get_students())
        else :
              return self.return_fail_with_not_found()
   

        