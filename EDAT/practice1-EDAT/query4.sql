CREATE OR replace VIEW count_language 
AS 
  SELECT language_id, 
         Count(*) 
  FROM   film 
  GROUP  BY language_id; 

CREATE OR replace VIEW max_count 
AS 
  SELECT Max(count) 
  FROM   count_language; 

SELECT "language"."name" 
FROM   "language", 
       max_count, 
       count_language 
WHERE  count_language.count = max_count.max 
       AND count_language.language_id = "language".language_id 












