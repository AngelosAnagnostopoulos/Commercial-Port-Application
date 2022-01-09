import mysql.connector
from mysql.connector import errorcode
from . import info,schema,insertions


def database_init(cursor):
        #Create tables and add foreign key constraints. 
        for table_name in schema.TABLES:
            table_description = schema.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
                    exit(1)
            else:
                print("OK")

        for constraint in schema.CONSTRAINTS:
            const_description = schema.CONSTRAINTS[constraint]
            try:
                print("Adding constraint {}: ".format(constraint), end='')
                cursor.execute(const_description)
            except mysql.connector.Error as err:
                if err.errno == 1005:
                    print("Constraint already satisfied")
                else:
                    print(err)
                    exit(1)
     

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(info.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def use_database(cursor):
    try:
        cursor.execute("USE {}".format(info.DB_NAME))
        print("Using db {}".format(info.DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exist.".format(info.DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(info.DB_NAME))
            mydb.database = info.DB_NAME
        else:
            print(err)
            exit(1)


def insertions(cursor):
    for i in range(len(insertions.insert_sql)):
        cursor.execute(insertions.insert_sql[i], multi=True)
