from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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

# Function to remove all entries
def remove_all_entries():
    with app.app_context():
        db.session.query(Product).delete()
        db.session.commit()
        print("All entries removed.")

if __name__ == '__main__':
    remove_all_entries()
