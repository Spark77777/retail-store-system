USE retail_store;

DELIMITER $$

CREATE TRIGGER reduce_stock
AFTER INSERT ON Sales_Item
FOR EACH ROW
BEGIN
    UPDATE Product
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END $$

DELIMITER ;
