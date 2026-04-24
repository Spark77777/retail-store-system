USE retail_store;

-- View all products
SELECT * FROM Product;

-- Total sales amount
SELECT SUM(total_amount) AS total_sales FROM Sales;

-- Best selling products
SELECT p.name, SUM(si.quantity) AS total_sold
FROM Sales_Item si
JOIN Product p ON si.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold DESC;

-- Low stock products
SELECT name, stock_quantity
FROM Product
WHERE stock_quantity < 20;

-- Customer purchase history
SELECT c.name, s.sale_id, s.sale_date
FROM Sales s
JOIN Customer c ON s.customer_id = c.customer_id;
