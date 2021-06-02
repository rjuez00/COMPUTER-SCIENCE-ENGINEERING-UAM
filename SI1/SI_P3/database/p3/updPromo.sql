ALTER TABLE customers 
ADD promo double precision NOT NULL
CONSTRAINT promo_default DEFAULT 0;

CREATE OR REPLACE FUNCTION func_updPromo() RETURNS TRIGGER AS $$
DECLARE
BEGIN
    /*sabemos que el TG_OP no es necesario pero es por si acaso 
    cambiamos el trigger a que salte con insert y delete*/
    IF TG_OP = 'UPDATE' THEN
        PERFORM pg_sleep(10);

        UPDATE orderdetail
        SET price = (products.price * (1-NEW.promo/100))
        FROM products
        WHERE 
            products.prod_id = orderdetail.prod_id AND
            orderdetail.orderid IN (
                SELECT orderid /*obtener el/los carritos de esta persona*/
                FROM orders
                WHERE 
                    orders.customerid = NEW.customerid 
                    AND orders.status is NULL);

    END IF;
    RETURN NEW;
END;
$$ LANGUAGE "plpgsql";


DROP TRIGGER IF EXISTS tr_updPromo ON customers;

CREATE TRIGGER tr_updPromo
BEFORE UPDATE ON customers
FOR EACH ROW EXECUTE PROCEDURE func_updPromo();