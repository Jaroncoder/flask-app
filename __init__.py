from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration for the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/my_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the db
    db.init_app(app)

    # Register blueprints or add routes here if you have any
    # from .routes import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    return app
