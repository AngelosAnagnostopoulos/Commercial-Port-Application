import mysql.connector
from mysql.connector import errorcode
from utils import dbutils, schema, info


config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "raise_on_warnings": True
    }

def main():

    try:
        mydb = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username/password combination")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = mydb.cursor()
        
        dbutils.use_database(cursor)
        dbutils.database_init(cursor)    
        
        test = "SHOW TABLES"
        cursor.execute("{}".format(test))

        for x in cursor:
            print(x)

        cursor.close()
        mydb.close() 


if __name__ == "__main__":
    main()
