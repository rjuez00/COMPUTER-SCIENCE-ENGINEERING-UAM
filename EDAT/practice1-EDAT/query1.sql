CREATE OR replace VIEW listofrental 
AS 
  SELECT Extract(year FROM rental_date) AS rental_year 
  FROM   rental; 

SELECT rental_year, 
       Count(rental_year) 
FROM   listofrental 
GROUP  BY ( rental_year ) 
