\echo 'TABLA DE ALERTAS:'
SELECT *
FROM alertas;
\echo 'CANTIDAD DE STOCK'
SELECT 
    prod_id, 
    stock, 
    sales
FROM inventory
WHERE prod_id = 1;


\echo '\n\nCREANDO CARRITO PARA TESTEAR'
INSERT INTO orders
    (orderid, 
    orderdate,
    customerid,
    netamount,
    tax,
    totalamount,
    status)
VALUES
    (999999, 
    NOW(), 
    1,
    0,
    21,
    0,
    '');

INSERT INTO orderdetail
    (orderid,
    prod_id,
    price,
    quantity)
VALUES
    (999999,
    1,
    14,
    406);

\echo 'PAGANDO EL ORDER'
UPDATE orders
SET status = 'Paid'
WHERE orderid = 999999;

\echo '\n\nTABLA DE ALERTAS:'
SELECT *
FROM alertas;
\echo 'CANTIDAD DE STOCK'
SELECT prod_id, stock, sales
FROM inventory
WHERE prod_id = 1;
\echo 'COMPROBAR QUE LA FECHA ES LA ACTUAL'
SELECT orderdate
FROM orders
WHERE 
    orderid = 999999

