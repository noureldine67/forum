# Import utils
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import os


def create_app():
    """
    Création de l'application web
    """

    # Initialisation de l'application Flask
    app = Flask(__name__)

    # Sécuriser la session cookie pour plus de sécurité
    # Assure que le cookie de session n'est envoyé que sur des connexions HTTPS
    app.config["SESSION_COOKIE_SECURE"] = (
        False  
    )

    # Empêche l'accès au cookie par JavaScript (sécurise contre les attaques XSS)
    app.config["SESSION_COOKIE_HTTPONLY"] = (
        True  
    )

    # Sécurise contre les attaques CSRF en restreignant l'envoi des cookies
    app.config["SESSION_COOKIE_SAMESITE"] = (
        "Lax"  
    )

    # Clé secrète pour sécuriser les sessions et les formulaires
    app.config["SECRET_KEY"] = os.urandom(
        32
    )  
    
    # Lien de connexion à la base de données
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    app.config["MONGO_URI"] = (
        f"mongodb+srv://{username}:{password}@cluster0.kaxfyuy.mongodb.net/forum?retryWrites=true&w=majority&appName=Cluster0"
    )

    # Bootstrap
    bootstrap = Bootstrap(app)

    # Protection CSRF pour sécuriser les formulaires
    csrf = CSRFProtect(app)

    # Mise en place d'un limiteur
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["5 per minute"],
    )

    # Base de données MongoDB
    mongo = PyMongo(app)

    # Renvoyer l'application, le limiteur et la base de données
    return app, limiter, mongo
