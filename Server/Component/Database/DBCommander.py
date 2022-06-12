from re import L
from Component.Logger import Logger
from Component.Database.DBConnection import DBConnection

class DBCommander(): 
    
    
    def query_data(self,command):

        
        print('Database # : Start query sql with command {}'.format(command))
        Logger().info('Database # : Start query sql with command {}'.format(command))
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
            query_data = [dict(row) for row in record_from_db]
        print('Database # : End query sql with data {}'.format(query_data))
        Logger().info('Database # : End query sql with data {}'.format(query_data))
        return query_data
        
    def execute(self,command):
        Logger().info('Database # : Start execute sql with command {}'.format(command))
        print('Database # : Start execute sql with command {}'.format(command))
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
        
        
        return True