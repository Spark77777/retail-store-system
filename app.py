from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Connect to PostgreSQL (Render DATABASE_URL)
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
cursor = conn.cursor()

# ✅ Create table automatically (IMPORTANT for mobile users)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2),
    stock_quantity INT DEFAULT 0
)
""")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

# Get all products
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

    # basic validation
    if not data.get('name') or not data.get('price') or not data.get('qty'):
        return jsonify({"error": "Missing fields"}), 400

    cursor.execute(
        "INSERT INTO Product(name, price, stock_quantity) VALUES (%s,%s,%s)",
        (data['name'], data['price'], data['qty'])
    )
    conn.commit()

    return jsonify({"message": "Product added"})

# Sell product
@app.route('/sell', methods=['POST'])
def sell():
    data = request.json

    # prevent negative stock
    cursor.execute("SELECT stock_quantity FROM Product WHERE product_id = %s", (data['id'],))
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Product not found"}), 404

    current_stock = result[0]
    if int(data['qty']) > current_stock:
        return jsonify({"error": "Not enough stock"}), 400

    cursor.execute(
        "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
        (data['qty'], data['id'])
    )
    conn.commit()

    return jsonify({"message": "Sale done"})

# Health check (useful for Render)
@app.route('/health')
def health():
    return "OK"

# Required for Render
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
