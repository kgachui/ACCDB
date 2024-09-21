import pyodbc 

class database:
    def __init__(self, driver: str,
                 server: str,
                 user_id: str,
                 password: str,
                 database: str,
                 db_table: str):
    
        self.__db_table = db_table
        self.cnxn = pyodbc.connect(Driver=driver,
                                   Server=server,
                                   UID=user_id,
                                   PWD=password,
                                   Database=database,
                                   TrustServerCertificate="yes")
        


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