CREATE OR replace VIEW rental_language 
AS 
  SELECT rental.rental_id, 
         inventory.film_id, 
         film.language_id 
  FROM   rental, 
         inventory, 
         film 
  WHERE  rental.inventory_id = inventory.inventory_id 
         AND inventory.film_id = film.film_id; 

CREATE OR replace VIEW language_count 
AS 
  SELECT "language"."name", 
         Count(*) 
  FROM   rental_language, 
         "language" 
  WHERE  rental_language.language_id = "language"."language_id" 
  GROUP  BY rental_language.language_id, 
            "language"."name"; 

CREATE OR replace VIEW count_max 
AS 
  SELECT Max(count) 
  FROM   language_count; 

SELECT language_count."name" 
FROM   language_count, 
       count_max 
WHERE  count_max.max = language_count.count 
