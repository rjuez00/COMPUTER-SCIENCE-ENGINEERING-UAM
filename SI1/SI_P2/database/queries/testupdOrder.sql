

INSERT INTO orders
	(orderid, orderdate, customerid,
	netamount, tax, totalamount, status)
VALUES
	(999999, NOW(), 653, 10, 21, 12.1, '');
                            
SELECT *
FROM orders
WHERE status = '';


INSERT INTO orderdetail
	(orderid,
	prod_id,
	price,
	quantity)
VALUES
	(999999,
	103,
	13,
	2);


SELECT *
FROM orders
WHERE status = '';
