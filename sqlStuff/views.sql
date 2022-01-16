CREATE VIEW EmployeeInfo AS
SELECT
    F_Name,
    L_Name,
    Salary,
    StartsAt,
    Finishes
FROM
    Shift,Starts_,Personel
WHERE
    Starts_.PersonelID = Personel.PersonelID AND Starts_.ShiftID = Shift.ShiftID;

CREATE VIEW CargoInfo AS
SELECT
    S_Name,
    Product,
    Amount,
    TransactionDate
FROM
    Regarding, Shipment,Transaction_,Ship,Completes
WHERE
    Ship.ShipID = Completes.ShipID AND Completes.TransactionID = Transaction_.TransactionID AND Shipment.ShipmentID = Regarding.ShipmentID AND Transaction_.TransactionID = Regarding.TransactionID;

CREATE VIEW AllShipsView AS
SELECT
    ShipID,
    S_Name,
    Flag,
    PosID
FROM Ship LEFT JOIN Position_ USING(ShipID);


CREATE VIEW ShipsInPort AS
SELECT * FROM AllShipsView
WHERE PosID IS NOT NULL;

CREATE VIEW ArrivingSoon AS
SELECT
    Ship.ShipID,
    S_Name,
    Flag,
    ArrivalDate
FROM 
    Ship,Arival
WHERE 
    Arival.ShipID = Ship.ShipID;

CREATE VIEW DepartingSoon AS
SELECT
    Ship.ShipID,
    S_Name,
    Flag,
    DepartureDate
FROM 
    Ship,Departure
WHERE 
    Departure.ShipID = Ship.ShipID;

CREATE VIEW PositionsView AS
SELECT 
    PosID, 
    PierID, 
    ShipID,
    S_Name
FROM Position_ LEFT JOIN Ship USING(ShipID);

CREATE VIEW UnauthorisedShipView AS
SELECT
    COUNT(S_Name) AS ShipsInPort
FROM 
    ShipsInPort;

CREATE VIEW UnauthorisedPersonelView AS
SELECT
    COUNT(*) AS Active_Personel
FROM 
    Personel;
