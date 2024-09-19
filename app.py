from flask import Flask, request, redirect, url_for, render_template_string, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_of_measurement = db.Column(db.String(20), nullable=False)

# Create the database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Create tables if they don't exist
create_tables()

# Route to view products
@app.route('/products')
def view_products():
    products = Product.query.all()
    
    return render_template_string('''
        <h1>All Products</h1>
        {% with messages = get_flashed_messages(with_categories=True) %}
            {% if messages %}
                <ul>
                    {% for category, message in messages %}
                        <li class="{{ category }}">{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Unit of Measurement</th>
                <th>Action</th>
            </tr>
            {% for product in products %}
            <tr>
                <td>{{ product.name }}</td>
                <td>{{ product.description }}</td>
                <td>${{ product.price }}</td>
                <td>{{ product.quantity }}</td>
                <td>{{ product.unit_of_measurement }}</td>
                <td><a href="{{ url_for('purchase_product', product_id=product.id) }}">Buy</a></td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">Back to Home</a></p>
    ''', products=products)

# Route to add a new product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        unit_of_measurement = request.form['unit_of_measurement']
        
        new_product = Product(name=name, description=description, price=float(price), quantity=int(quantity), unit_of_measurement=unit_of_measurement)
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template_string('''
        <h1>Add New Product</h1>
        <form method="POST">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            
            <label for="description">Description:</label><br>
            <textarea id="description" name="description"></textarea><br><br>
            
            <label for="price">Price:</label><br>
            <input type="number" id="price" name="price" step="0.01" required><br><br>
            
            <label for="quantity">Quantity:</label><br>
            <input type="number" id="quantity" name="quantity" required><br><br>
            
            <label for="unit_of_measurement">Unit of Measurement:</label><br>
            <input type="text" id="unit_of_measurement" name="unit_of_measurement" required><br><br>
            
            <input type="submit" value="Add Product">
        </form>
        <p><a href="/">Back to Home</a></p>
    ''')

# Route to handle purchase of a product
@app.route('/purchase/<int:product_id>')
def purchase_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product is available
    if product.quantity > 0:
        # Decrease the quantity of the product
        product.quantity -= 1
        db.session.commit()
        
        # Flash a purchase successful message
        flash('Purchase successful!', 'success')
    else:
        # Flash a purchase failed message
        flash('Product out of stock!', 'error')
    
    return redirect(url_for('view_products'))

# Route to view and buy products
@app.route('/buy')
def buy_products():
    products = Product.query.all()
    
    return render_template_string('''
        <h1>Buy Products</h1>
        {% with messages = get_flashed_messages(with_categories=True) %}
            {% if messages %}
                <ul>
                    {% for category, message in messages %}
                        <li class="{{ category }}">{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Unit of Measurement</th>
                <th>Action</th>
            </tr>
            {% for product in products %}
            <tr>
                <td>{{ product.name }}</td>
                <td>{{ product.description }}</td>
                <td>${{ product.price }}</td>
                <td>{{ product.quantity }}</td>
                <td>{{ product.unit_of_measurement }}</td>
                <td><a href="{{ url_for('purchase_product', product_id=product.id) }}">Buy</a></td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">Back to Home</a></p>
    ''', products=products)

# Route for the home page
@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome to the UZHAVI</h1>
        <p><a href="/products">View Products</a></p>
        <p><a href="/add_product">Add New Product</a></p>
        <p><a href="/buy">Buy Products</a></p>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
