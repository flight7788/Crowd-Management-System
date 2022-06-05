import firebase_admin
from firebase_admin import credentials

class FireStoreInitializer():  
   
    def __init__(self ,key_chain):
        cred = credentials.Certificate(key_chain)
        firebase_admin.initialize_app(cred)
        
    

     