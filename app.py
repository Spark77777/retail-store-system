from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2),
    stock_quantity INT DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INT,
    quantity INT,
    price NUMERIC(10,2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

# Get products
@app.route('/products')
def get_products():
    cursor.execute("SELECT * FROM Product ORDER BY product_id")
    rows = cursor.fetchall()

    products = []
    for r in rows:
        products.append({
            "product_id": r[0],
            "name": r[1],
            "price": float(r[2]),
            "stock_quantity": r[3]
        })

    return jsonify(products)

# Add product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json

    if not data or not data.get('name') or not data.get('price') or not data.get('qty'):
        return jsonify({"error": "Missing fields"}), 400

    cursor.execute(
        "INSERT INTO Product(name, price, stock_quantity) VALUES (%s,%s,%s)",
        (data['name'], data['price'], data['qty'])
    )
    conn.commit()

    return jsonify({"message": "Product added"})

# Sell product (with sales tracking)
@app.route('/sell', methods=['POST'])
def sell():
    data = request.json

    if not data or not data.get('id') or not data.get('qty'):
        return jsonify({"error": "Invalid request"}), 400

    cursor.execute(
        "SELECT stock_quantity, price FROM Product WHERE product_id = %s",
        (data['id'],)
    )
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Product not found"}), 404

    stock, price = result

    if int(data['qty']) > stock:
        return jsonify({"error": "Not enough stock"}), 400

    # Record sale
    cursor.execute(
        "INSERT INTO Sales(product_id, quantity, price) VALUES (%s,%s,%s)",
        (data['id'], data['qty'], price)
    )

    # Update stock
    cursor.execute(
        "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
        (data['qty'], data['id'])
    )

    conn.commit()

    return jsonify({"message": "Sale recorded"})

# Delete product
@app.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.json

    if not data or not data.get('id'):
        return jsonify({"error": "Invalid request"}), 400

    cursor.execute("DELETE FROM Product WHERE product_id = %s", (data['id'],))
    conn.commit()

    return jsonify({"message": "Product deleted"})

# Total sales
@app.route('/total_sales')
def total_sales():
    cursor.execute("SELECT SUM(quantity * price) FROM Sales")
    total = cursor.fetchone()[0] or 0

    return jsonify({"total_sales": float(total)})

# Health
@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
