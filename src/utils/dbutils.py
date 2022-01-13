import mysql.connector
from mysql.connector import errorcode
from . import info,schema


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
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'UTF8MB4'".format(info.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def use_database(database, cursor):
    try:
        cursor.execute("USE {}".format(info.DB_NAME))
        print("Using db {}".format(info.DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exist.".format(info.DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(info.DB_NAME))
            database.database = info.DB_NAME
        else:
            print(err)
            exit(1)


def execute_sql_file(conn, cursor, filepath):

    with open(filepath, 'r', encoding='utf-8') as insertions:
        # Potential for injection here, should be fine as long as an end user doesnt have access
        sql_commands = insertions.read().split(';')
        
        for command in sql_commands:
            try:
                cursor.execute(command)
                conn.commit()
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    print("1062")
                elif err.errno == 1065:
                    print("Empty query.")
                else:
                    print(err)
                    exit(1)

def insertions(conn, cursor):
    #Read directly from .sql file and insert data into base. 
    import os
    # cur_path = os.path.dirname(__file__)
    # print(cur_path)
    # print(os.getcwd())
    path = os.path.relpath("sqlStuff/insertions.sql")
    path = os.path.normpath(path)
    #print(path)
    print("Opening insertions file...")
    with open(path, 'r', encoding='utf-8') as insertions:
        #Do stuff here
        sql_commands = insertions.read().split(';')
        print("Inserting data...")
        for command in sql_commands:
            try:
                cursor.execute(command)
                conn.commit()
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    print("Already added values.")
                else:
                    print(err)
                    exit(1)











