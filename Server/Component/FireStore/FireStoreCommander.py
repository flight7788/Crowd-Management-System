from firebase_admin import firestore
from Component.Logger import Logger
import threading
from datetime import datetime

class FireStoreCommander():  
   
   
   
      # 子執行緒類別
    class TranscationThread(threading.Thread):
      def __init__(self, method, collection , data={}):
        threading.Thread.__init__(self)
        self.method  = method
        self.collection = collection
        self.data = data

      def run(self):
        if self.method == 'delete':
          print('#Server :')
          Logger().info("Start Transaction: method: {}, collection: {} , data {}".format(self.method,self.collection,self.data))
          self.collection.delete()
          Logger().info("Transacion End")
          
        if self.method == 'update':
          Logger().info("Start Transaction: method: {}, collection: {} , data {}".format(self.method,self.collection,self.data))
          self.collection.update(self.data)
          Logger().info("Transacion End")
          
        if self.method == 'insert':
          Logger().info("Start Transaction: method: {}, collection: {} , data {}".format(self.method,self.collection,self.data))
          self.collection.set(self.data)
          Logger().info("Transacion End")
          
        
    
    def __init__(self):
        self.client = firestore.client()
    
    
    # Get last id of a collection
    def get_collection_last_idx(self,collection_name):
        last_idx =0
        try:
          
          query_data = {}
          datas = self.client.collection(collection_name).get()
          for data in datas:
             query_data[data.id]=data.to_dict() 
             
          last_idx = sorted([int(x) for x in query_data.keys()])[-1]

        except Exception as e:
          print('{}'.format(e))
        finally:
          return last_idx

    # Query data in Collection
    #  Method:
    #   Query all data in         : query(collection_name = COLLECTION)
    #   Query by document id      : query(collection_name = COLLECTION , id = ID)
    #   Query by column condition : query(collection_name = COLLECTION , column_name = COLUMN_NAME , key_word = KEY_WORD)
    #  (where column_name=keyword)
    
    
    def query(self,collection_name, id = None, column_name = None , key_word = None):
        query_data={}
        is_success = True
        error_message = ''
        try:
          print('{} : {}'.format(datetime.now(),'start query froim firebase'))
          
          if(id!= None):
            self.client.collection(collection_name).doc(id).get()
          else:
            datas = self.client.collection(collection_name).where(column_name ,'==' ,key_word).get()
            
          print('{} : {}'.format(datetime.now(),'end query froim firebase'))
          
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
      
      
    # Insert data into collection  
    def insert(self,collection_name,data):
        id = self.get_collection_last_idx(collection_name) + 1
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          self.TranscationThread('insert',current_document,data).start()
          #current_document.set(data)
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
      
      
    # Update data by document id in a collection
    def update(self,collection_name,id,data):
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          self.TranscationThread('update',current_document,data).start()
          #current_document.update(data)
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
    
    
    # Delete data by document id in a collection
    def delete(self,collection_name,id):
        current_document = self.client.collection(collection_name).document(str(id))
        is_success = True
        error_message = ''
        try:
          self.TranscationThread('delete',current_document).start()
          #current_document.delete()
        except Exception as e:
          is_success = False
          error_message = '{}'.format(e)
        finally:
          return self.return_data_processor(is_success,error_message,'')
      
      
    # Pack data into a specific format
    def return_data_processor(self,is_success,message,data):
        return {'is_success' : is_success , 'message' : message , 'data' : data }\
          
          
          
    def query_last_one(self,collection_name, id = None, column_name = None , key_word = None):
        query_data={}
        is_success = True
        error_message = ''
        try:
          print('{} : {}'.format(datetime.now(),'start query froim firebase'))
          
          if(id!= None):
            self.client.collection(collection_name).doc(id).get()
          else:
            datas = self.client.collection(collection_name).where(column_name ,'==' ,key_word).order_by("time").limit_to_last(1).get()
            
          print('{} : {}'.format(datetime.now(),'end query froim firebase'))
          
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
      

     

    
            
        

        
        
        
    