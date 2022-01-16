import mysql.connector,logging
from mysql.connector import errorcode
from utils import dbutils,info

import os

config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "raise_on_warnings": True
    }

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
        
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('information.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    try:
        mydb = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username/password combination")
            logger.info("Wrong username/password combination")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.info("Database does not exist")
        else:
            logger.critical(err)
    else:
        cursor = mydb.cursor(buffered=True)
        
        try:
            cursor.execute("DROP DATABASE projectDB")
        except:
            pass

        
        os.chdir(os.path.dirname(__file__))

        dbutils.use_database(mydb, cursor)        
        print("Creating tables:")
        dbutils.execute_sql_file(mydb, cursor, "../sqlStuff/dbcreation.sql")
        print("Inserting data:")
        dbutils.execute_sql_file(mydb, cursor, "../sqlStuff/insertions.sql")
        
        dbutils.execute_sql_file(mydb, cursor,"../sqlStuff/randomShips.sql")
        print("Creating views:")
        dbutils.execute_sql_file(mydb, cursor, "../sqlStuff/views.sql")
        print("Creating ships index:")
        dbutils.execute_sql_file(mydb, cursor, "../sqlStuff/indexes.sql")

        mydb.commit()
        
        test = "SHOW TABLES"
        cursor.execute("{}".format(test))

        for x in cursor:
            print(x)
        
        cursor.close()
        mydb.close() 

if __name__ == "__main__":
    main()
