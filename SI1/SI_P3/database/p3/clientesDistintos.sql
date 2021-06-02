/*Función que devuelve el número de clientes que, en un año y mes dado, han realizado*/
/*pedidos por un importe mayor a umbral*/
DROP INDEX IF EXISTS ordersindex;
CREATE INDEX ordersindex ON orders(totalamount, (EXTRACT(YEAR FROM orderdate)), EXTRACT(MONTH FROM orderdate));

CREATE OR REPLACE FUNCTION clientesDistintos(umbral INTEGER, yyyymm TEXT)
  RETURNS integer AS $$

DECLARE
BEGIN

return (SELECT 
            COUNT(DISTINCT customerid) as clients
        FROM orders
        WHERE 
            totalamount > $1  /*hacemos un slice del year y del month y los comparamos*/
            AND EXTRACT(YEAR FROM orderdate) = CAST( SUBSTRING(yyyymm, 1,4) AS double precision)
            AND EXTRACT(MONTH FROM orderdate) = CAST( SUBSTRING(yyyymm, 5,6) AS double precision)
        );

END;
$$ LANGUAGE "plpgsql";

SELECT clientesDistintos(100, '201504')




