import sys
import logging
import pymysql
import json
import os


class database:
    def __init__(self, rds_proxy_host: str,
                 user_id: str,
                 password: str,
                 database: str,
                 db_table: str):
    
        self.__db_table = db_table
        self.cnxn = pymysql.connect(host=rds_proxy_host, user=user_id, passwd=password, db=database, connect_timeout=5)
        


    def insert_data(self, dataset: list[dict]):
        #self.cnxn.cursor().execute((f'SELECT * FROM {self.__db_table}'))
        for datarows in dataset:
            columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in datarows.keys())
            values = ', '.join("'" + str(x) + "'" for x in datarows.values())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (self.__db_table, columns, values)
            sql = sql.replace ( "`","")             
            self.cnxn.cursor().execute(sql)
        self.cnxn.cursor().commit()



# Example usage:
if __name__ == "__main__":
    db=database()
    connection = db.cnxn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM table')

    for row in cursor:
        print('row = %r' % (row,))