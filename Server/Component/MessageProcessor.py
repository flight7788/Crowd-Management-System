class MessageProcessor:
        
    def return_success(self):
        return {'status' : 'Success'}
    
    def return_success_with_data(self,data):
        return {'status' : 'Success' , 'data' : data}
        
    def return_fail(self):
        return {'status' : 'Fail' }
    
    def return_fail_with_reason(self,reason):
        return {'status' : 'Fail' , 'reason' : reason}
        
      