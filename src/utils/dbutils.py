#! python3
#Utility functions for mysql connector.

import mysql.connector
from mysql.connector import errorcode
from . import info


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
                    print("Duplicate entry on database.")
                elif err.errno == 1065:
                    print("Empty query.")
                elif err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already exists.")
                elif err.errno == 1005:
                    print("Constraint already satisfied.")
                else:
                    print(err)
                    exit(1)


