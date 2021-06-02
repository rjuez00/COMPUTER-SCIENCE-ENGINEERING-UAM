/*Declarar función con sus argumentos*/
CREATE OR REPLACE FUNCTION func_updOrders() RETURNS TRIGGER AS $$
DECLARE
process_orderid integer;
BEGIN
    /*Si el trigger ha saltado por insertar, actualiza las orders sumandoles al netamount y al totalamount la cantidad correspondiente*/
    IF TG_OP = 'INSERT' THEN
        UPDATE orders
        SET netamount = ROUND(
                CAST(
                    netamount + NEW.quantity * NEW.price
                    AS numeric),
                    2
            ),
            totalamount = ROUND(
                CAST(
                    totalamount + (tax/100 +1) * NEW.quantity * NEW.price
                    AS numeric),
                    2
            )

        WHERE
            orders.orderid = NEW.orderid;
        RETURN NEW;

    /*Si el trigger ha saltado por actualizar, actualiza las orders sumandoles o restándoles al netamount y al totalamount la cantidad correspondiente*/
    /*dependiendo de la diferencia entre OLD.quantity y NEW.quantity*/
    ELSIF TG_OP = 'UPDATE' THEN
        process_orderid := OLD.orderid;

        UPDATE orders
        SET netamount = ROUND(
                CAST(
                    netamount - (OLD.quantity - NEW.quantity) * NEW.price
                    AS numeric),
                    2
            ),
            totalamount = ROUND(
                CAST(
                    totalamount - (tax/100 +1) * (OLD.quantity - NEW.quantity) * NEW.price
                    AS numeric),
                    2
            )



        WHERE
            orders.orderid = process_orderid;
        RETURN NEW;

    /*Si el trigger ha saltado por borrar, actualiza las orders restándoles al netamount y al totalamount la cantidad correspondiente de los productos borrados*/
    ELSIF TG_OP = 'DELETE' THEN
        process_orderid := OLD.orderid;

        UPDATE orders
        SET netamount = ROUND(
                CAST(
                    netamount - (OLD.quantity * OLD.price)
                    AS numeric),
                    2
            ),
            totalamount = ROUND(
                CAST(
                    totalamount - (tax/100 +1) * (OLD.quantity * OLD.price)
                    AS numeric),
                    2
            )

        WHERE
            orders.orderid = process_orderid;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE "plpgsql";


DROP TRIGGER IF EXISTS tr_updOrders ON orderdetail;

/*Declarar trigger que se activa antes de insertar,actualizar o borrar en orderdetail*/
CREATE TRIGGER tr_updOrders
BEFORE
INSERT
OR
UPDATE
OR
DELETE ON orderdetail
FOR EACH ROW EXECUTE PROCEDURE func_updOrders();