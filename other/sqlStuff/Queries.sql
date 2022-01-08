SELECT S_Name,Flag FROM Ship;
SELECT S_Name FROM Ship WHERE PrevPort = 'Delhi, India';
SELECT AVG(DWT), MAX(GT) FROM Ship;

SELECT * FROM Position_;

SELECT S_Name,Flag FROM Ship,Arival WHERE Ship.ShipID = Arival.ShipID AND ArivalDate > current_date();
SELECT S_Name,Flag FROM Ship WHERE PosID IS NOT NULL;
SELECT * FROM Ship NATURAL JOIN Completes NATURAL JOIN Transaction_ NATURAL JOIN Regarding NATURAL JOIN Shipment;

SELECT S_Name,Flag FROM Ship NATURAL JOIN Completes NATURAL JOIN Transaction_ NATURAL JOIN Regarding NATURAL JOIN Shipment WHERE TransactionDate BETWEEN 
       DATE ('1931-01-01') AND DATE_SUB(NOW(), INTERVAL 1 DAY);
       
SELECT F_name,L_name FROM Personel NATURAL JOIN Starts_ NATURAL JOIN Shift WHERE StartsAt BETWEEN NOW() AND DATE ('2023-02-10');