CREATE OR replace VIEW inventorybob 
AS 
  SELECT inventory.inventory_id 
  FROM   actor, 
         film_actor, 
         inventory 
  WHERE  actor.actor_id = film_actor.actor_id 
         AND actor.first_name = 'Bob' 
         AND actor.last_name = 'Fawcett' 
         AND film_actor.film_id = inventory.film_id; 

CREATE OR replace VIEW inventory_rented 
AS 
  SELECT rental.rental_id, 
         inventory.inventory_id, 
         inventory.store_id 
  FROM   inventorybob, 
         rental, 
         inventory 
  WHERE  inventorybob.inventory_id = rental.inventory_id 
         AND rental.inventory_id = inventory.inventory_id; 

CREATE OR replace VIEW citystore 
AS 
  SELECT store.store_id, 
         city.city 
  FROM   "address", 
         store, 
         city 
  WHERE  store.address_id = "address".address_id 
         AND "address".city_id = city.city_id; 

SELECT DISTINCT citystore.city 
FROM   citystore 
       join inventory_rented 
         ON inventory_rented.store_id = citystore.store_id 
