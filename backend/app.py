# app.py
from flask import Flask
from flask_cors import CORS
from src.steganography_routes import steganography_bp

app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(steganography_bp)

if __name__ == '__main__':
    app.run(debug=True)