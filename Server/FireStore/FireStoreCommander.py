from email.mime import message
from firebase_admin import firestore

class FireStoreCommander():  
   
    def __init__(self):
        self.client = firestore.client()
    
    #取得目前集合最新的資料id
    def get_collection_last_idx(self,collection_name):
        current_size =0
        try:
          collection = self.client.collection(collection_name).get()
          count = len(collection)
          current_size = int(collection[count - 1].id)
        except Exception as e:
          print('{}'.format(e))
        finally:
          return current_size

    #查詢資料
    def query(self,collection_name, id = None, column_name = None , key_word = None):
        query_data={}
        is_success = True
        error_message = ''
        try:
          datas = self.client.collection(collection_name).get()
          for data in datas:
             query_data[data.id]=data.to_dict() 
           
          if column_name != None and key_word != None :
             new_dict = {}
             for key, value in query_data.items():
                 if(column_name in value):
                     if(value[column_name]==key_word):
                         new_dict[key] = value
             query_data = new_dict
              
          if id != None : 
             query_data= query_data[str(id)]
           
           
           
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,query_data)
      
    #插入資料  
    def insert(self,collection_name,data):
        id = self.get_collection_last_idx(collection_name) + 1
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          current_document.set(data)
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
      
    #更新資料
    def update(self,collection_name,id,data):
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          current_document.update(data)
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
    
    #刪除資料 
    def delete(self,collection_name,id):
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          current_document.delete()
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
      
    #整理成統一回傳格式
    def return_data_processor(self,is_success,message,data):
        return { 'is_success' : is_success , 'message' : message , 'data' : data }
      

     

    
            
        

        
        
        
    