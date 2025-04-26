from flask import Flask
from src.routes import steganography_routes

# Initialize the Flask app
app = Flask(__name__)

# Register blueprints for route handling
app.register_blueprint(steganography_routes, url_prefix='/steganography')

if __name__ == '__main__':
    app.run(debug=True)
