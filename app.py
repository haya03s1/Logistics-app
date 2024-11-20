from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

# Initialize Flask app and database
app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supply_chain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Factory model
class Factory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=False)
    offers_space = db.Column(db.Boolean, default=False)
    available_space = db.Column(db.Float, default=0.0)  # in square meters
    required_space = db.Column(db.Float, default=0.0)  # if requesting space
    subscription_paid = db.Column(db.Boolean, default=False)  # Subscription status

    def __repr__(self):
        return f"<Factory {self.name}>"

# Subscription model (for tracking subscription payments)
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'), nullable=False)
    amount = db.Column(db.Float, default=18750.0)  # 18,750 SAR annual fee
    paid = db.Column(db.Boolean, default=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    factory = db.relationship('Factory', backref='subscriptions')

# Warehouse Request model
class WarehouseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requesting_factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'), nullable=False)
    offering_factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'), nullable=False)
    space_allocated = db.Column(db.Float, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="PENDING")

# Create tables (if they don't already exist)
with app.app_context():
    db.create_all()

# Route: Factory login and submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        location = request.form['location']
        offers_space = request.form.get('offers_space') == 'on'
        available_space = float(request.form['available_space'])
        required_space = float(request.form['required_space'])

        # Check if the factory already exists by email
        existing_factory = Factory.query.filter_by(email=email).first()
        if existing_factory:
            return jsonify({"message": f"Welcome back {existing_factory.name}!"}), 200

        # Save factory info (if new factory)
        new_factory = Factory(
            name=name,
            email=email,
            location=location,
            offers_space=offers_space,
            available_space=available_space,
            required_space=required_space
        )
        db.session.add(new_factory)
        db.session.commit()

        return jsonify({"message": f"Thank you {name} for your submission!"}), 200

    return render_template('factory_login.html')

# Route: Get available materials for purchase
@app.route('/materials', methods=['GET'])
def get_materials():
    materials = [
        {"name": "Steel", "price": 500},
        {"name": "Aluminum", "price": 400},
        {"name": "Plastic", "price": 200}
    ]
    return jsonify(materials)

# Route: Add to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    # Assume data contains factory id, material name, quantity, etc.
    factory_id = data['factory_id']
    material_name = data['material_name']
    quantity = data['quantity']
    price = data['price']  # Per item price

    # Here we should calculate total cost, and add to cart
    total_cost = price * quantity

    # For simplicity, just returning the total cost
    return jsonify({"message": f"Added {quantity} {material_name}(s) to the cart.", "total_cost": total_cost})

# Route: Checkout and subscription
@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    factory_id = data['factory_id']

    # Fetch the factory and check if subscription is paid
    factory = Factory.query.get(factory_id)
    if not factory.subscription_paid:
        return jsonify({"message": "Subscription not paid. Please pay the subscription fee."}), 400

    # Assume we process payment and finalize checkout here
    return jsonify({"message": "Checkout completed successfully!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
