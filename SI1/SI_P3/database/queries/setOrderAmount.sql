/*Declarar función con sus argumentos*/
CREATE OR REPLACE FUNCTION setOrderAmount() RETURNS void AS $$
    /*Actualiza orders con el netamount y el totalamount correspondiente*/
    UPDATE orders
    SET    netamount = results.netamount,
           totalamount = results.totalamount
    FROM   (        /*Selecciona los orderdetails con su precio neto toltal (precio*cantidad)*/
                    /*y su totalamount total, (precio*cantidad*impuestos), ordenado por orderid*/
                    SELECT      orderdetail.orderid,
                                Sum(price * quantity)                                        AS netamount,
                                Round(Cast(Sum(price * quantity)*(1+tax/100) AS NUMERIC), 2) AS totalamount
                    FROM       orderdetail
                    INNER JOIN orders ON
                        orders.orderid = orderdetail.orderid
                    GROUP BY
                        orderdetail.orderid,
                        tax
            ) AS results
    WHERE  orders.orderid = results.orderid
$$ LANGUAGE SQL;


SELECT setOrderAmount();