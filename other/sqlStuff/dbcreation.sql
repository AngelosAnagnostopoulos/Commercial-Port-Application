/*CREATE DATABASE limanidb;*/
/*DROP DATABASE limanidb;*/

DROP TABLE WeatherInfo;
DROP TABLE Starts_;
DROP TABLE Shift;
DROP TABLE Containership;
DROP TABLE Tanker;
DROP TABLE Other;
DROP TABLE Commercial;
DROP TABLE Arival;
DROP TABLE Departure;
DROP TABLE Completes;
DROP TABLE Ship;
DROP TABLE Position_;
DROP TABLE Pier;
DROP TABLE Location;
DROP TABLE Regarding;
DROP TABLE Shipment;
DROP TABLE Personel;
DROP TABLE Container;
DROP TABLE Transaction_;


CREATE TABLE Location
(
  LocID INT ,
  Country VARCHAR(255) ,
  Lattitude FLOAT ,
  Longtitude FLOAT ,
  City VARCHAR(255) ,
  LocTime FLOAT ,
  PRIMARY KEY (LocID)
);

CREATE TABLE WeatherInfo 
(
  Temperature FLOAT ,
  HasIce INT ,
  HasWaves INT ,
  Winds FLOAT ,
  LocID INT ,
  FOREIGN KEY (LocID) REFERENCES Location(LocID) 
);

CREATE TABLE Position_
(
  PosID INT ,
  MaxSize FLOAT ,
  Taken INT ,
  PierID INT,
  PRIMARY KEY (PosID)
);

CREATE TABLE Ship
(
  ShipID INT ,
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

CREATE TABLE Shipment 
(
  ShipmentID INT ,
  Product VARCHAR(255) ,
  PRIMARY KEY (ShipmentID)
);

CREATE TABLE Pier
(
  PierID INT ,
  TotalPositions INT ,
  LocID INT ,
  PRIMARY KEY (PierID),
  FOREIGN KEY (LocID) REFERENCES Location(LocID)
);

ALTER TABLE Position_
ADD CONSTRAINT PierLink
FOREIGN KEY (PierID) REFERENCES Pier(PierID);


CREATE TABLE Shift 
(
  ShiftID INT ,
  StartsAt DATE ,
  Finishes DATE ,
  PierID INT ,
  ShipID INT ,
  PRIMARY KEY (ShiftID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) , 
  FOREIGN KEY (PierID) REFERENCES Pier(PierID) 
);


CREATE TABLE Personel 
(
  PersonelID INT ,
  Salary INT ,
  F_Name VARCHAR(255) ,
  L_Name VARCHAR(255) ,
  SupervisorID INT,
  PRIMARY KEY (PersonelID)
);

ALTER TABLE Personel
ADD CONSTRAINT Supervisor
FOREIGN KEY (SupervisorID) 
REFERENCES Personel(PersonelID) ;


CREATE TABLE ContainerShip
(
  ShipID INT ,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) 
);
CREATE TABLE Tanker
(
  TankID INT,
  PRIMARY KEY (TankID),
  FOREIGN KEY (TankID) REFERENCES Ship(ShipID)
);
CREATE TABLE Commercial
(
  ShipID INT ,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) 
);
CREATE TABLE Other
(
  ShipID INT ,
  PRIMARY KEY (ShipID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) 
);

CREATE TABLE Transaction_
(
  TransactionID INT ,
  TransactionDate DATE ,
  HasContainer BOOLEAN ,
  PRIMARY KEY (TransactionID)
);

CREATE TABLE Starts_
(
  ShiftID INT ,
  PersonelID INT ,
  PRIMARY KEY (ShiftID, PersonelID),
  FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)  ,
  FOREIGN KEY (PersonelID) REFERENCES Personel(PersonelID) 
);

CREATE TABLE Completes
(
  ShipID INT ,
  TransactionID INT ,
  PRIMARY KEY (ShipID, TransactionID),
  FOREIGN KEY (ShipID) REFERENCES Ship(ShipID) ,
  FOREIGN KEY (TransactionID) REFERENCES Transaction_(TransactionID) 
);

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

CREATE TABLE Container
(
  ContainerID INT ,
  FOREIGN KEY (ContainerID) REFERENCES Transaction_(TransactionID) 
);

