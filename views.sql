USE retail_store;

CREATE VIEW sales_summary AS
SELECT 
    s.sale_id,
    c.name AS customer_name,
    s.sale_date,
    SUM(si.quantity * si.price) AS total_amount
FROM Sales s
JOIN Customer c ON s.customer_id = c.customer_id
JOIN Sales_Item si ON s.sale_id = si.sale_id
GROUP BY s.sale_id;
