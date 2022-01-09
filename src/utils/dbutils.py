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
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(info.DB_NAME))
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
            mydb.database = info.DB_NAME
        else:
            print(err)
            exit(1)


def insertions(cursor):
    for i in range(len(insert_sql)):
        try:
            cursor.execute(insert_sql[i], multi=True)
        except mysql.connector.Error as err:
            if err.errno == 1062:
                print("Already added values.")
            else:
                print(err)
                exit(1)

insert_sql = []

loc = "INSERT INTO Location VALUES('Greece', 0.0,0.0,'Piraeus',20.34,1);"
weath = "INSERT INTO WeatherInfo VALUES(10.5,0,1,3.0,1 );"
pers = """
INSERT INTO Personel VALUES
	('1','1500','Νίκος','Κούκος',NULL),
	('2','1500','Νίκος','Κορόμπος','1'),
	('3','1500','Νίκος','Καβουρδίκης','1'),
	('4','1500','Νίκος','Καρδιβούρκος','1'),
	('5','1500','Χρήστος','Παπαναστασίου','1'),
	('6','1500','Θεμιστοκλής','Φωτόπουλος','1');"""
    
pier = """
INSERT INTO Pier VALUES
	('1','5','1'),
    ('2','5','1');"""

pos = """
    INSERT INTO Position_ VALUES
(30.0,1,1,1),
(20.0,1,2,1),
(10.0,0,3,1),
(50.0,0,4,1),
(300.0,1,5,1),
(200.0,1,6,2),
(100.0,0,7,2),
(500.0,0,8,2),
(500.0,1,9,2),
(500.0,1,10,2);"""

ship = """
    INSERT INTO Ship VALUES
('Delhi, India', 48.0, DATE '2014-02-03','India','DurgaSS',133,1,10,100,NULL),
('Piraeus, Greece', NULL, DATE '2000-01-01','Greek','Noor1',50,2,3,30,1),
('Moscow, Russia', NULL, DATE '2014-02-03','Pakistan','ScamSS',420,3,30,200,2),
('Okinawa, Japan', 1000, DATE '1942-08-27','American','U.S.S. William D. Porter',115,4,40,100,NULL ),
('Delhi, India', 48.0, DATE '2014-02-03','India','NesoSS',133,5,10,100,NULL ),
('Delhi, India', NULL, DATE '1965-02-06','Greek','Noor2ElectricBoogaloo',25,6,300,30,6),
('Moscow, Russia', NULL, DATE '2014-02-03','Armenian','Tenkian',15,7,30,200,9 ),
('Piraeus, Greece', 24, DATE '1963-02-21','American','U.S.S Phill McCracken',140,8,40,100,NULL ),
('Piraeus, Greece', 24, DATE '1962-04-25','American','S.S. Naomi',100,9,50,90,NULL ),
('Tokyo, Japan', NULL, DATE '2014-04-11','Japanesse','Nakatomi Plaza',89,10,40,100,10 ),
('Tokyo, Japan', NULL, DATE '2000-02-24','Armenian','The lady of the oceans',86,11,40,100,5 ),
('Tokyo, Japan', 24, DATE '1963-02-21','Armenian','SuperAFM',62,12,40,100,NULL ),
('Piraeus, Greece', 24, DATE '1963-02-21','American','S.S. DistroTube',123,13,40,100,NULL ),
('Piraeus, Greece', 24, DATE '1963-02-21','American','S.S. Thryalidis',1521,14,40,100,NULL );"""

shift = """
    INSERT INTO Shift VALUES
	(DATE '2022-02-10', DATE '2022-02-11', 1,1,1),
	(DATE '2022-02-10', DATE '2022-02-11', 2,1,2),
	(DATE '2022-02-10', DATE '2022-02-11', 3,2,10);"""

starts = """

INSERT INTO Starts_ VALUES
	(1,1),
    (2,2);"""

dept = "INSERT INTO Departure VALUES (1,DATE '2022-02-02',FALSE,NULL,2,3);"

arr = """

INSERT INTO Arival VALUES
	(1,DATE '2022-02-10',DATE '2022-02-15',FALSE,NULL,2,10),
    (2,DATE '2022-02-11',DATE '2022-02-16',FALSE,NULL,3,9),
	(3,DATE '2010-02-02',NULL,TRUE,NULL,4,5);"""
    
tank = "INSERT INTO Tanker VALUES('3'),('2'),('1');"
cont = "INSERT INTO ContainerShip VALUES('12'),('10'),('11');"
other = "INSERT INTO Other VALUES('5'),('4');"
comm = "INSERT INTO Commercial VALUES('6'),('7'),('8'),('9');"

trans = """
INSERT INTO Transaction_ VALUES 
(1,DATE '2000-02-02',FALSE),
(2,DATE '2001-01-01',TRUE),
(3,DATE '2022-02-10', TRUE);"""

completes = """

INSERT INTO Completes VALUES
(4,2),
(2,1),
(5,3); """

container = """INSERT INTO Container VALUES 
(1),
(2);"""

shipment = """
    INSERT INTO Shipment VALUES
('Sugar', 1),
('Silk', 2),
('Coal',3);"""

regarding = """
    INSERT INTO Regarding VALUES
(1,2.5,200,1,1),
(1,2.5,200,2,2),
(100,1.5,1,3,3);"""

insert_sql.append(loc)
insert_sql.append(weath)
insert_sql.append(pers)
insert_sql.append(pier)
insert_sql.append(pos)
insert_sql.append(ship)
insert_sql.append(arr)
insert_sql.append(dept)
insert_sql.append(shift)
insert_sql.append(starts)
insert_sql.append(comm)
insert_sql.append(other)
insert_sql.append(cont)
insert_sql.append(tank)
insert_sql.append(trans)
insert_sql.append(completes)
insert_sql.append(container)
insert_sql.append(shipment)
insert_sql.append(regarding)




















