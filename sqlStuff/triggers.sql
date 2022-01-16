CREATE TRIGGER depart_ship
    AFTER UPDATE ON Position_ FOR EACH ROW

    BEGIN
        IF NEW.ShipID IS NULL AND OLD.ShipID IS NOT NULL
        THEN
            INSERT INTO Departure (DepartureDate, Completed, ShipID, PosID) 
            VALUES (NOW(), 1, OLD.ShipID, OLD.PosID);
        END IF;
    END
||
CREATE TRIGGER arrive_ship
    AFTER UPDATE ON Position_ FOR EACH ROW
    BEGIN
        IF NEW.ShipID IS NOT NULL AND OLD.ShipID IS NULL
        THEN
            INSERT INTO Arival (ArrivalDate, Completed, ShipID, PosID)
            VALUES (NOW(), 1, NEW.ShipID, NEW.PosID);
        END IF;
    END
