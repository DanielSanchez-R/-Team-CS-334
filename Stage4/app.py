from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teashop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enmudan8@gmail.com'
app.config['MAIL_PASSWORD'] = 'kftowimrjckmohqc'
app.config['MAIL_DEFAULT_SENDER'] = 'enmudan8@gmail.com'

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    items = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Template routes
@app.route('/')
def home():
    return redirect(url_for('main'))

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/checkout.html')
def checkout():
    return render_template('checkout.html')

@app.route('/guestcheckout.html')
def guest_checkout():
    return render_template('guestcheckout.html')

@app.route('/payment.html')
def payment():
    return render_template('payment.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manager.html')
def manager():
    return render_template('manager.html')

@app.route('/orders.html')
def orders():
    return render_template('orders.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

# Product APIs
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'image': p.image} for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'], image=data['image'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'})

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if product:
        product.name = data['name']
        product.price = data['price']
        product.image = data['image']
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    return jsonify({'error': 'Product not found'}), 404

# Order APIs
@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'full_name': o.full_name, 'email': o.email, 'items': o.items, 'status': o.status} for o in orders])

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.json
    order = Order(full_name=data['full_name'], email=data['email'], items=str(data['items']), status='Pending')
    db.session.add(order)
    db.session.commit()
    send_receipt(data['email'], data['full_name'], data['items'])
    return jsonify({'message': 'Order placed and email sent'})

@app.route('/api/orders/<int:id>', methods=['PUT'])
def mark_order_complete(id):
    order = Order.query.get(id)
    if order:
        order.status = 'Completed'
        db.session.commit()
        return jsonify({'message': 'Order marked as completed'})
    return jsonify({'error': 'Order not found'}), 404

# User APIs
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'password': u.password, 'email': u.email} for u in users])

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Missing credentials'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# Public API
@app.route('/public/api/products', methods=['GET'])
def public_products():
    products = Product.query.all()
    return jsonify([{'name': p.name, 'price': p.price} for p in products])

# Static and service workers
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/static/assets/<path:filename>')
def static_assets(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'assets'), filename)

# Email sending helper
def send_receipt(email, name, items):
    try:
        item_list = "\n".join([f"{i['name']} x{i['quantity']} - ${i['price']} each" for i in items])
        total = sum(i['price'] * i['quantity'] for i in items)
        msg = Message('Your New Mexico Tea Shop Receipt', recipients=[email])
        msg.body = f"Thank you for your order, {name}!\n\nItems:\n{item_list}\n\nTotal: ${total:.2f}\n\nEnjoy your tea!"
        mail.send(msg)
    except Exception as e:
        print("Failed to send email:", e)

# DB creation
def create_tables():
    db.create_all()
    if Product.query.count() == 0:
        seed_products()

def seed_products():
    seed_data = [
        {'name': "New Mexico Green Tea", 'price': 5.99, 'image': "/static/assets/greentea.jpeg"},
        {'name': "New Mexico Black Tea", 'price': 6.99, 'image': "/static/assets/blacktea.jpeg"},
        {'name': "New Mexico Peppermint Tea", 'price': 7.49, 'image': "/static/assets/pepperminttea.jpeg"},
        {'name': "New Mexico Chamomile Tea", 'price': 5.49, 'image': "/static/assets/chamomiletea.jpeg"},
        {'name': "New Mexico Hibiscus Tea", 'price': 6.79, 'image': "/static/assets/hibiscustea.jpeg"},
        {'name': "New Mexico Mint Tea", 'price': 5.89, 'image': "/static/assets/minttea.jpeg"},
        {'name': "New Mexico Chai Tea", 'price': 7.99, 'image': "/static/assets/chaitea.jpeg"},
        {'name': "New Mexico White Tea", 'price': 8.49, 'image': "/static/assets/whitetea.jpeg"},
        {'name': "New Mexico Oolong Tea", 'price': 9.49, 'image': "/static/assets/oolongtea.jpeg"},
        {'name': "New Mexico Cinnamon Buns", 'price': 4.99, 'image': "/static/assets/cinnamonbuns.jpeg"}
    ]
    for data in seed_data:
        db.session.add(Product(name=data['name'], price=data['price'], image=data['image']))
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
