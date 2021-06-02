/*Declarar función con sus argumentos*/
CREATE OR REPLACE FUNCTION func_updInventory() RETURNS TRIGGER AS $$
DECLARE
BEGIN
    IF NEW.STATUS <> 'Paid' OR OLD.STATUS <> '' THEN
        RETURN NEW;
    END IF;
    
    /*Resto y sumo las cantidades del pedido*/
    UPDATE inventory
    SET 
        sales = sales + products.quantity,
        stock = stock - products.quantity
    FROM ( /*obtengo las cantidades del orderdetails*/
        SELECT prod_id, quantity
        FROM orderdetail
        WHERE orderid = NEW.orderid
    ) as products
    WHERE products.prod_id = inventory.prod_id;

    /*Actualizamos la fecha a la de hoy*/
    NEW.orderdate = NOW();

    /*Cuando ya tenemos los stock actualizado solo tenemos que obtener los que 
    tienen stock 0 y es del order que se ha actualizado*/
    INSERT INTO alertas(prod_id)
        SELECT orderdetail.prod_id
        FROM inventory
        INNER JOIN orderdetail ON
            inventory.prod_id = orderdetail.prod_id
        WHERE 
            inventory.stock = 0
            AND orderdetail.orderid = NEW.orderid;

    RETURN NEW;
   

END;
$$ LANGUAGE "plpgsql";


DROP TRIGGER IF EXISTS tr_updInventory ON orders;

/*Declarar trigger que se activa antes de actualizar en orders*/
CREATE TRIGGER tr_updInventory
BEFORE
UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE func_updInventory();