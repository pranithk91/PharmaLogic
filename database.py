
import mysql.connector
from mysql.connector import Error
import time
from datetime import date

start_time = time.time()

def db_cursor(): 
    try:
        conn = mysql.connector.connect(
            host="193.203.184.152",
            port='3306',
            user="u885517842_AdminUser",
            password="MdP@ssword!!1",
            database="u885517842_MedicalStore"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            cursor = conn.cursor()
            return cursor, conn
        
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

def selectTable(table_name, column_names = '*', condition= "1=1", Limit=None):
    
    cursor, conn = db_cursor()
    if Limit == None:
        query = "SELECT " + column_names + " FROM " + table_name + " WHERE " + condition
    else:
        query = "SELECT " + column_names + " FROM " + table_name + " WHERE " + condition + " LIMIT " + str(Limit)
    
    try:
        print(query)
        cursor.execute(query)
        results = cursor.fetchall()
   
        if 'connection' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MariaDB connection is closed")
        return results
    except Error as e:
        print(query)
        print(f'Error in executing query: {e}')
    
def insertIntoTable(table_name, values, column_names ):
    cursor, conn = db_cursor()
    query = "INSERT INTO " + table_name + " (" + column_names + ")" + " VALUES " + values 
    print(query)
    try:
        cursor.execute(query)
        conn.commit()

        if 'connection' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MariaDB connection is closed")
        
    except Error as e:
        print(f'Error in executing query: {e}')

def getClientID(currentName):
    
    NCount = selectTable('vw_Name_Counter', 'last_id', condition=f"starting_letter = '{currentName[0]}'" )
    NCount = f"{NCount[0][0]+1:03}"
    clientID = str(date.today().strftime("%y"))+str(date.today().strftime("%m"))+str(currentName[0]).upper()+str(NCount)
    return clientID

def runQuery(query, condition):
    
    cursor, conn = db_cursor()
    updateQuery = query + ' where ' + condition
    try:
        print(updateQuery)
        cursor.execute(updateQuery)
        conn.commit()
        results = cursor.fetchall()
   
        if 'connection' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MariaDB connection is closed")
        return results
    except Error as e:
        print(query)
        print(f'Error in executing query: {e}')



end_time = time.time()

#print(end_time-start_time)