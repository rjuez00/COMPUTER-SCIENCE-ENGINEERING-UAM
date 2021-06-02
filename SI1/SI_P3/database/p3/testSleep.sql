SELECT customerid
FROM customers
WHERE customerid=7;

SELECT *
FROM orders
WHERE orders.customerid=7
LIMIT 2;

SELECT *
FROM orders
NATURAL JOIN orderdetail
WHERE orders.customerid = 7
LIMIT 2;