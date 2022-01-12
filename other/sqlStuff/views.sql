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

CREATE VIEW ShipsInPort AS
SELECT
    S_Name,
    Flag,
    PosID
FROM Ship
WHERE Ship.PosID IS NOT NUlL;

CREATE VIEW ArrivingSoon AS
SELECT
    S_Name,
    Flag,
    ArivalDate
FROM 
    Ship,Arival
WHERE 
    Arrival.ShipID = Ship.ShipID AND ArrivalDate BETWEEN NOW() AND (NOW() + INTERVAL 7 DAY);

CREATE VIEW DepartingSoon AS
SELECT
    S_Name,
    Flag,
    DepartureDate
FROM 
    Ship,Departure
WHERE 
    Departure.ShipID = Ship.ShipID AND DepartureDate BETWEEN NOW() AND (NOW() + INTERVAL 7 DAY);

CREATE VIEW UnauthorisedShipView AS
SELECT
    COUNT(S_Name) AS ShipsInPort
FROM 
    Ship
WHERE Ship.PosID IS NOT NULL;

CREATE VIEW UnauthorisedPersonelView AS
SELECT
    COUNT(*) AS Active_Personel
FROM 
    Personel;
