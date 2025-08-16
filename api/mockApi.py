from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Fake database
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 750},
    {"id": 2, "name": "Phone", "price": 500}
]

CART = []

# LOGIN (returns JWT)
import os

app = Flask(__name__)

# Generate a new secret each time server restarts
app.config["JWT_SECRET_KEY"] = os.urandom(24)  # 24 random bytes
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") and data.get("password"):
        token = create_access_token(identity=data["username"])
        return jsonify(token=token)
    return jsonify(error="Invalid credentials"), 401

@app.route("/products")
@jwt_required()
def products():
    return jsonify(PRODUCTS), 200

# ADD TO CART (protected)
@app.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    product_id = request.get_json().get("id")
    CART.append(product_id)
    return jsonify({"cart": CART}), 200

# PLACE ORDER (protected)
@app.route("/order", methods=["POST"])
@jwt_required()
def order():
    user = get_jwt_identity()
    return jsonify({"message": f"Order placed by {user}", "cart": CART}), 200

if __name__ == "__main__":
    app.run(debug=True)
