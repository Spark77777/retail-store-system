USE retail_store;

-- Suppliers
INSERT INTO Supplier (supplier_name, contact, address) VALUES
('ABC Traders', '9876543210', 'Mysore'),
('Fresh Foods', '9123456780', 'Bangalore');

-- Products
INSERT INTO Product (name, category, price, stock_quantity, supplier_id) VALUES
('Rice', 'Grocery', 50, 100, 1),
('Milk', 'Dairy', 25, 50, 2),
('Soap', 'Personal Care', 30, 70, 1);

-- Customers
INSERT INTO Customer (name, phone, email) VALUES
('Ravi', '9999999999', 'ravi@email.com'),
('Anu', '8888888888', 'anu@email.com');

-- Sales
INSERT INTO Sales (sale_date, customer_id, total_amount) VALUES
(CURDATE(), 1, 0);

-- Sales Items
INSERT INTO Sales_Item (sale_id, product_id, quantity, price) VALUES
(1, 1, 2, 50),
(1, 2, 1, 25);
