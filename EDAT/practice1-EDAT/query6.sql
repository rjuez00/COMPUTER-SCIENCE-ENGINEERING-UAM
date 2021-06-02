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

CREATE OR replace VIEW maxcustomer 
AS 
  SELECT rentalcount.customer_id, 
         count 
  FROM   rentalcount, 
         maxcount 
  WHERE  maxcount.max = rentalcount.count; 

CREATE OR replace VIEW vip_category 
AS 
  SELECT maxcustomer.customer_id, 
         film_category.category_id 
  FROM   maxcustomer, 
         inventory, 
         rental, 
         film_category 
  WHERE  rental.customer_id = maxcustomer.customer_id 
         AND rental.inventory_id = inventory.inventory_id 
         AND inventory.film_id = film_category.film_id; 

CREATE OR replace VIEW vip_count_category 
AS 
  SELECT customer_id, 
         category_id, 
         Count(category_id) 
  FROM   vip_category 
  GROUP  BY category_id, 
            customer_id 
  ORDER  BY count DESC; 

CREATE OR replace VIEW vip_max_count 
AS 
  SELECT customer_id, 
         Max(count) 
  FROM   vip_count_category 
  GROUP  BY customer_id; 

CREATE OR replace VIEW finished_but_with_id 
AS 
  SELECT vip_max_count.customer_id, 
         vip_count_category.category_id, 
         vip_count_category.count 
  FROM   vip_max_count, 
         vip_count_category 
  WHERE  vip_max_count.max = vip_count_category.count 
         AND vip_max_count.customer_id = vip_count_category.customer_id; 

SELECT customer.first_name, 
       customer.last_name, 
       category.name 
FROM   finished_but_with_id, 
       category, 
       customer 
WHERE  finished_but_with_id.customer_id = customer.customer_id 
       AND finished_but_with_id.category_id = category.category_id 
