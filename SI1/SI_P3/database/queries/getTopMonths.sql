/*Declarar función con sus argumentos*/
CREATE OR REPLACE FUNCTION getTopMonths(num_products int, importe int) RETURNS TABLE (Año DOUBLE PRECISION, Mes DOUBLE PRECISION, Importe NUMERIC, Productos BIGINT) AS $$
  
  SELECT *
  FROM (  SELECT
            /*Devuelve el año, mes, importe acumulado y productos acumulados, agrupados por año y mes*/
            EXTRACT(year from orders.orderdate) as Año,
            EXTRACT(month from orders.orderdate) as Mes,
            sum(orders.totalamount) as Importe,
            sum(orderdetail.quantity) as Productos
          FROM orderdetail
          INNER JOIN orders ON
            orderdetail.orderid = orders.orderid
          GROUP BY
              Año,
              Mes
        ) as result

  WHERE
      /*Filtrar por productos e importe de los por argumentos*/
      result.Productos >= $1
      OR result.Importe >= $2;

$$ LANGUAGE SQL;