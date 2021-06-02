INSERT INTO orders
	(orderid, orderdate, customerid,
	netamount, tax, totalamount, status)
VALUES
	(999999, NOW(), 653, 10, 21, 12.1, NULL);
	/*creamos carrito*/

/*insertamos orderdetails*/
INSERT INTO orderdetail
	(orderid, prod_id, price, quantity)
VALUES
	(999999, 1, 13, 1);

INSERT INTO orderdetail
	(orderid, prod_id, price, quantity)
VALUES
	(999999, 2, 15, 1);

INSERT INTO orderdetail
	(orderid, prod_id, price, quantity)
VALUES
	(999999, 3, 18, 1);

\echo '\n\nPrecios antes de la promo:'

/*printeamos los precios antes*/
SELECT orderid, prod_id, price
FROM orderdetail
WHERE
	orderid = 999999;

\echo '\n\nPromo de 40%'
/*hacemos que salte el trigger*/
UPDATE customers
SET promo = 40
WHERE customerid = 653;


/*imprimimos los precios despues*/
SELECT orderid, prod_id, price
FROM orderdetail
WHERE
	orderid = 999999;