from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Fake products (later you can replace with a database)
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 500},
    {"id": 2, "name": "Headphones", "price": 50},
    {"id": 3, "name": "Keyboard", "price": 30},
]

# Make cart count available everywhere
@app.context_processor
def inject_cart_count():
    return {"cart_count": len(session.get("cart", []))}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)

@app.route("/cart")
def cart():
    return render_template("cart.html", cart=session.get("cart", []))

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        cart.append(product)
        session["cart"] = cart
        flash(f"Added {product['name']} to cart", "success")
    return redirect(url_for("products"))

@app.route("/clear_cart")
def clear_cart():
    session["cart"] = []
    flash("Cart cleared!", "info")
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)
