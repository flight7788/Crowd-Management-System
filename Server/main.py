

from FireStore.FireStoreConnector import FireStoreInitializer
from FireStore.FireStoreCommander import FireStoreCommander
from Entity.StudentProfile import StudentProfile

FIRESTORE_KEYCHAIN = "connection_info.json"



def main():
    
    FireStoreInitializer(FIRESTORE_KEYCHAIN)
    db = FireStoreCommander()
    
    StudentProfile(db).add_student('何翊宇','100000')
    print(StudentProfile(db).get_students())
    
    
    #print(db.insert(collection_name='student_profile',data={'name':'123','stu':'heyiyu'}))
    #print(db.update(collection_name='student_profile',id=4,data={'name':'111','stu':'111111'}))
    #print(db.delete(collection_name='student_profile',id=4))
    #print(db.query(collection_name='student_profile',column_name = 'name', key_word='111'))
    #print(db.query(collection_name='student_profile',id=1))
    
    
    

main()