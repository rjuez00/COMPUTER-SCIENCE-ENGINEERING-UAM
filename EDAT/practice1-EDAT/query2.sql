CREATE OR replace VIEW rentalcount 
AS 
  SELECT customer_id, 
         Count(*) 
  FROM   rental 
  GROUP  BY customer_id; 

CREATE OR replace VIEW maxcount 
AS 
  SELECT Max(count) 
  FROM   rentalcount; 

SELECT customer.customer_id, 
       first_name, 
       last_name, 
       count 
FROM   rentalcount, 
       maxcount, 
       customer 
WHERE  maxcount.max = rentalcount.count 
       AND rentalcount.customer_id = customer.customer_id 
