from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)

    # Configuration de la connexion à MongoDB
    app.config['MONGO_URI'] = os.getenv(
        'MONGO_URI', 'mongodb://localhost:27017/3icp')

    # Initialiser la connexion MongoDB
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_database()

    # Configurer CORS
    CORS(app)

    print('=============', os.getenv(
        'MONGO_URI', 'mongodb://localhost:27017/3icp'))
    # Enregistrer les blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
