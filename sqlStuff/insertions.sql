INSERT INTO Location VALUES(1,'Greece',0,0,'Piraeus',CURTIME());
INSERT INTO WeatherInfo VALUES(10.5,0,1,3.0,1 );

INSERT INTO Personel VALUES
	('1','1500','Νίκος','Κούκος',NULL),
	('2','1500','Νίκος','Κορόμπος','1'),
	('3','1500','Νίκος','Καβουρδίκης','1'),
	('4','1500','Νίκος','Καρδιβούρκος','1'),
	('5','1500','Χρήστος','Παπαναστασίου','1'),
	('6','1500','Θεμιστοκλής','Φωτόπουλος','1');

INSERT INTO Pier VALUES
	('1','5','1'),
    ('2','5','1');
    
INSERT INTO Ship VALUES
(1,'Delhi, India', NULL, DATE '2014-02-03','India','DurgaSS',133,10,100),
(2,'Piraeus, Greece', NULL, DATE '2000-01-01','Greek','Noor1',50,3,30),
(3,'Moscow, Russia', NULL, DATE '2014-02-03','Pakistan','ScamSS',420,30,200),
(4,'Okinawa, Japan', NULL, DATE '1942-08-27','American','U.S.S. William D. Porter',115,40,100),
(5,'Delhi, India', NULL, DATE '2014-02-03','India','NesoSS',133,10,100),
(6,'Delhi, India', NULL, DATE '1965-02-06','Greek','Noor2ElectricBoogaloo',25,300,30),
(7,'Moscow, Russia', NULL, DATE '2014-02-03','Armenian','UltimateSmashBros',15,30,200),
(8,'Piraeus, Greece', NULL, DATE '1963-02-21','American','U.S.S Phill McCracken',140,40,100),
(9,'Piraeus, Greece', NULL, DATE '1962-04-25','American','S.S. Naomi',100,50,90),
(10,'Tokyo, Japan', NULL, DATE '2014-04-11','Japanesse','Nakatomi Plaza',89,40,100),
(11,'Tokyo, Japan', NULL, DATE '2000-02-24','Armenian','The lady of the oceans',86,40,100),
(12,'Tokyo, Japan', NULL, DATE '1963-02-21','Armenian','SuperAFM',62,40,100),
(13,'Piraeus, Greece', NULL, DATE '1963-02-21','American','S.S. DistroTube',12,40,100),
(14,'Piraeus, Greece', NULL, DATE '1963-02-21','American','S.S. Thryalidis',1521,40,100);

INSERT INTO Position_ VALUES
(1,30.0,1,1, 2),
(2,20.0,1,1, 3),
(3,10.0,0,1, NULL),
(4,50.0,0,1, NULL),
(5,300.0,1,1, 11),
(6,200.0,1,2, 6),
(7,100.0,0,2, NULL),
(8,500.0,0,2, NULL),
(9,500.0,1,2, 7),
(10,500.0,1,2, 10);

INSERT INTO Shift VALUES
	(1,DATE '2022-02-10', DATE '2022-02-11', 1,1),
	(2,DATE '2022-02-10', DATE '2022-02-11', 1,2),
	(3,DATE '2022-02-10', DATE '2022-02-11', 2,10);

INSERT INTO Starts_ VALUES 
	(1,1),
    (2,2);
    
INSERT INTO Departure VALUES (1,DATE '2022-02-02',FALSE,NULL,2,3);

INSERT INTO Arival VALUES
	(1,DATE '2022-02-10',DATE '2022-02-15',FALSE,NULL,12,8),
    (2,DATE '2022-02-11',DATE '2022-02-16',FALSE,NULL,1,3);
    
INSERT INTO Tanker VALUES('3'),('2'),('1');
INSERT INTO ContainerShip VALUES('12'),('10'),('11');
INSERT INTO Other VALUES('5'),('4');
INSERT INTO Commercial VALUES('6'),('7'),('8'),('9');


INSERT INTO Transaction_ VALUES 
(1,DATE '2000-02-02',FALSE),
(2,DATE '2001-01-01',TRUE),
(3,DATE '2022-02-10', TRUE); /*TransID, TransDate,HasContainer*/

INSERT INTO Completes VALUES 
(4,2),
(2,1),
(5,3);  /*ShipID, TransID*/

INSERT INTO Container VALUES 
(1),
(2); /*ContainerID*/

INSERT INTO Shipment VALUES 
(1,'Sugar'),
(2,'Silk'),
(3,'Coal'); 

INSERT INTO Regarding VALUES 
(1,1,1,2.5,200),
(2,2,1,2.5,200),
(3,3,100,1.5,1); /*ShipmentID,TransID,Vol,Kg,Amount*/

