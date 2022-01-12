CONSTRAINTS = {}
CONSTRAINTS["PierLink"] = (
    """ALTER TABLE Position_
    ADD CONSTRAINT PierLink
    FOREIGN KEY (PierID) REFERENCES Pier(PierID);"""
    )
CONSTRAINTS["Supervisor"] = (
    """ALTER TABLE Personel
    ADD CONSTRAINT Supervisor
    FOREIGN KEY (SupervisorID) 
    REFERENCES Personel(PersonelID);""" 
    )

TABLES = {}
TABLES['Location'] = (
    """CREATE TABLE Location
(
  LocID INT NOT NULL AUTO_INCREMENT,
  Country VARCHAR(255) ,
  Lattitude FLOAT ,
  Longtitude FLOAT ,
  City VARCHAR(255) ,
  LocTime FLOAT ,
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
  PosID INT NOT NULL AUTO_INCREMENT,
  MaxSize FLOAT ,
  Taken INT ,
  PierID INT,
  PRIMARY KEY (PosID)
);
        """)
TABLES['Ship'] = ("""
        CREATE TABLE Ship
(
  ShipID INT NOT NULL AUTO_INCREMENT,
  PrevPort VARCHAR(255) ,
  EstimatedArrivalTime FLOAT,
  Constructed DATE ,
  Flag VARCHAR(255) ,
  S_Name VARCHAR(255) ,
  Length_ FLOAT ,
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
  ShipmentID INT NOT NULL AUTO_INCREMENT,
  Product VARCHAR(255) ,
  PRIMARY KEY (ShipmentID)
);
        """)
TABLES['Pier'] = ("""
CREATE TABLE Pier
(
  PierID INT NOT NULL AUTO_INCREMENT,
  TotalPositions INT ,
  LocID INT ,
  PRIMARY KEY (PierID),
  FOREIGN KEY (LocID) REFERENCES Location(LocID)
);

        """)
       
TABLES['Shift'] = ("""
CREATE TABLE Shift 
(
  ShiftID INT NOT NULL AUTO_INCREMENT,
  StartsAt DATE ,
  Finishes DATE ,
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
  PersonelID INT NOT NULL AUTO_INCREMENT,
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
  TransactionID INT NOT NULL AUTO_INCREMENT,
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
  ShipmentID INT ,
  TransactionID INT ,
  Volume FLOAT ,
  Weight FLOAT ,
  Amount FLOAT ,
  PRIMARY KEY (ShipmentID, TransactionID),
  FOREIGN KEY (ShipmentID) REFERENCES Shipment(ShipmentID)  ,
  FOREIGN KEY (TransactionID) REFERENCES Transaction_(TransactionID) 
);

        """)
TABLES['Arival'] = ("""
CREATE TABLE Arival
(
  ArrivalID INT NOT NULL AUTO_INCREMENT,
  ArrivalDate DATE ,
  EstimatedDeparture DATE DEFAULT NULL ,
  Completed BOOLEAN ,
  Delay DATE,
  ShipID INT ,
  PosID INT ,
  PRIMARY KEY (ArrivalID) ,
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) ,
  FOREIGN KEY (PosID) REFERENCES Position_(PosID) 
);

        """)
TABLES['Departure'] = ("""
CREATE TABLE Departure
(
  DepartureID INT NOT NULL AUTO_INCREMENT,
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
  ContainerID INT NOT NULL AUTO_INCREMENT,
  FOREIGN KEY (ContainerID) REFERENCES Transaction_(TransactionID) 
);
       
        """)

