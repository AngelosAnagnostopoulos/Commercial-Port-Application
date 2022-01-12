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
    Starts_.PersonelID = Personel.PersonelID AND Starts_.ShiftID = Shift.ShiftID


