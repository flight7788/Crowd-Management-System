from Component.Database.DBCommander import DBCommander
class StudentLog(DBCommander):  
    
    def get_logs(self):
        
        command = "SELECT a.*,b.name,b.id FROM logs a join profile b on a.card_no = b.card_no order by a.data_id desc ;"
        
        return self.query_data(command)
    
    
    def get_last_log_by_stu_id(self,id):
        
        command = "SELECT a.*,b.name,b.id FROM logs a join profile b on a.card_no = b.card_no where b.id = '{}' order by a.data_id desc  limit 1 ;".format(id)
        
        return self.query_data(command)
    
    def get_logs_by_card_no(self,card_no):
        
        command = "SELECT a.*,b.name,b.id FROM logs a join profile b on a.card_no = b.card_no where a.card_no = '{}' order by a.data_id desc ;".format(card_no)
        
        return self.query_data(command)
        
    def get_a_log(self,id):   
        
        command = "SELECT a.*,b.name,b.id FROM logs a join profile b on a.card_no = b.card_no where a.data_id = '{}' order by a.data_id desc  limit 1  ;".format(id)
        
        return self.query_data(command)
        
    def add_log(self, card_no='' , img='' , client_IP='' , action=''  ,  time='' ):
        
        
        command = "INSERT INTO logs (action,card_no,client_IP,img,time) VALUES  ('{}','{}','{}','{}','{}');".format(action,card_no,client_IP,img,time)
        return self.execute(command)
        
        
    def del_log(self,id):
        command = "delete from logs where data_id = '{}' ;".format(id)
        
        return self.execute(command)
    
