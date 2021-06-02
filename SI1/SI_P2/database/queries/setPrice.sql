/*Actualiza el precio de los orderdetail diminuyendo 2% el precio por año desde la orderdate*/
UPDATE orderdetail
SET price = Round(Cast(temporary.price * Pow(0.98, Extract(YEAR
                                                           FROM Now()) - Extract(YEAR
                                                                                 FROM temporary.orderdate)) AS NUMERIC), 2)
FROM
  /*Selecciona todos los orderid con su correspondientes prod_id, orderdate y price*/
  (SELECT orderdetail.orderid,
          orderdetail.prod_id,
          orderdate,
          products.price
   FROM orderdetail
   INNER JOIN orders ON orderdetail.orderid = orders.orderid
   INNER JOIN products ON orderdetail.prod_id = products.prod_id) AS
temporary
WHERE orderdetail.orderid = temporary.orderid
  AND orderdetail.prod_id = temporary.prod_id;