from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Connect to PostgreSQL (Render provides DATABASE_URL)
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
cursor = conn.cursor()

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
    cursor.execute(
        "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
        (data['qty'], data['id'])
    )
    conn.commit()
    return jsonify({"message": "Sale done"})

# Required for Render
if __name__ == "__main__":
    app.run()
