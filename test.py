import mysql.connector
from mysql.connector import errorcode

USER = "root"
HOST = "localhost"
DB_NAME = "projectDB"
PASSWORD = "1234"

TABLES = {}
TABLES['Location'] = (
    """CREATE TABLE Location
(
  Country VARCHAR(255) ,
  Lattitude FLOAT ,
  Longtitude FLOAT ,
  City VARCHAR(255) ,
  LocTime FLOAT ,
  LocID INT ,
  PRIMARY KEY (LocID)
);
        """)
TABLES['WeatherInfo'] = (
        """CREATE TABLE WeatherInfo 
(
  Temperature FLOAT ,
  HasIce INT ,
  HasWaves INT ,
  Winds FLOAT ,
  LocID INT ,
  FOREIGN KEY (LocID) REFERENCES Location(LocID) 
);
        """)
TABLES['Position'] = ("""CREATE TABLE Position_
(
  MaxSize FLOAT ,
  Taken INT ,
  PosID INT ,
  PierID INT,
  PRIMARY KEY (PosID)
);
        """)
TABLES['Ship'] = ("""
        CREATE TABLE Ship
(
  PrevPort VARCHAR(255) ,
  EstimatedArrivalTime FLOAT,
  Constructed DATE ,
  Flag VARCHAR(255) ,
  S_Name VARCHAR(255) ,
  Length_ FLOAT ,
  ShipID INT ,
  GT INT ,
  DWT INT ,
  PosID INT,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (PosID) REFERENCES Position_(PosID) 
);
        """)
TABLES['Shipment'] = ("""
CREATE TABLE Shipment 
(
  Product VARCHAR(255) ,
  ShipmentID INT ,
  PRIMARY KEY (ShipmentID)
);
        """)
TABLES['Pier'] = ("""
CREATE TABLE Pier
(
  PierID INT ,
  TotalPositions INT ,
  LocID INT ,
  PRIMARY KEY (PierID),
  FOREIGN KEY (LocID) REFERENCES Location(LocID)
);

        """)
       
TABLES['Shift'] = ("""
CREATE TABLE Shift 
(
  StartsAt DATE ,
  Finishes DATE ,
  ShiftID INT ,
  PierID INT ,
  ShipID INT ,
  PRIMARY KEY (ShiftID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) , 
  FOREIGN KEY (PierID) REFERENCES Pier(PierID) 
);
        """)

TABLES['Personel'] = ("""
CREATE TABLE Personel 
(
  PersonelID INT ,
  Salary INT ,
  F_Name VARCHAR(255) ,
  L_Name VARCHAR(255) ,
  SupervisorID INT,
  PRIMARY KEY (PersonelID)
);

        """)
#Disjoint#1
TABLES['ContainerShip'] = ("""
CREATE TABLE ContainerShip
(
  ShipID INT NOT NULL,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID)
);

        """)
TABLES['Commercial'] = ("""
CREATE TABLE Commercial
(
  ShipID INT NOT NULL,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID)
);

        """)
TABLES['Tanker'] = ("""
CREATE TABLE Tanker
(
  ShipID INT NOT NULL,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID)
);

        """)
TABLES['Other'] = ("""
CREATE TABLE Other
(
  ShipID INT NOT NULL,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID)
);

        """)

TABLES['Transaction'] = ("""
CREATE TABLE Transaction_
(
  TransactionID INT,
  TransactionDate DATE,
  HasContainer INT,
  PRIMARY KEY (TransactionID)
);

        """)
TABLES['Starts'] = ("""
CREATE TABLE Starts_
(
  ShiftID INT ,
  PersonelID INT ,
  PRIMARY KEY (ShiftID, PersonelID),
  FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)  ,
  FOREIGN KEY (PersonelID) REFERENCES Personel(PersonelID) 
);

        """)
TABLES['Completes'] = ("""
CREATE TABLE Completes
(
  ShipID INT ,
  TransactionID INT ,
  PRIMARY KEY (ShipID, TransactionID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) ,
  FOREIGN KEY (TransactionID) REFERENCES Transaction_(TransactionID) 
);
        """)
TABLES['Regarding'] = ("""
CREATE TABLE Regarding
(
  Volume FLOAT ,
  Weight FLOAT ,
  Amount FLOAT ,
  ShipmentID INT ,
  TransactionID INT ,
  PRIMARY KEY (ShipmentID, TransactionID),
  FOREIGN KEY (ShipmentID) REFERENCES Shipment(ShipmentID)  ,
  FOREIGN KEY (TransactionID) REFERENCES Transaction_(TransactionID) 
);

        """)
TABLES['Arival'] = ("""
CREATE TABLE Arival
(
  ArivalID INT ,
  ArivalDate DATE ,
  EstimatedDeparture DATE ,
  Completed BOOLEAN ,
  Delay DATE,
  ShipID INT ,
  PosID INT ,
  PRIMARY KEY (ArivalID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) ,
  FOREIGN KEY (PosID) REFERENCES Position_(PosID) 
);

        """)
TABLES['Departure'] = ("""
CREATE TABLE Departure
(
  DepartureID INT ,
  DepartureDate DATE ,
  Completed BOOLEAN ,
  Delay DATE,
  ShipID INT ,
  PosID INT ,
  PRIMARY KEY (DepartureID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) ,
  FOREIGN KEY (PosID) REFERENCES Position_(PosID) 
);

        """)
TABLES['Container'] = ("""
 CREATE TABLE Container
(
  Container INT NOT NULL,
  FOREIGN KEY (Container) REFERENCES Transaction_(TransactionID)
);
       
        """)


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

config = {
        "user":USER,
        "host":HOST,
        "password":PASSWORD,
        "raise_on_warnings": True
    }

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

    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("Using db {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exist.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            mydb.database = DB_NAME
        else:
            print(err)
            exit(1)
    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

#Wtf am i supposed to do w/ this shit? 
    p1 = """ALTER TABLE Position_
    ADD CONSTRAINT PierLink
    FOREIGN KEY (PierID) REFERENCES Pier(PierID);"""

    p2 = """ALTER TABLE Personel
    ADD CONSTRAINT Supervisor
    FOREIGN KEY (SupervisorID) 
    REFERENCES Personel(PersonelID);""" 


    try:
        cursor.execute(p1)
    except mysql.connector.Error as err:
        print(err)
 
    try:
        cursor.execute(p2)
    except mysql.connector.Error as err:
        print(err)
   
    ri = "SHOW TABLES"
    cursor.execute("{}".format(ri))

    for x in cursor:
        print(x)

    cursor.close()
    mydb.close()
