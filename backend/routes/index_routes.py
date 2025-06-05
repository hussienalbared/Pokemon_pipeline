"""
This module defines the index route for the Flask application.

Blueprints:
    index_bp (Blueprint): Handles the root ('/') route.

Routes:
    / : Returns a welcome message.
"""

from flask import Blueprint

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    """Return a welcome message for the default index page."""
    return "Welcome to the default index page!"
