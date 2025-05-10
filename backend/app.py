# app.py
from flask import Flask
from src.steganography_routes import steganography_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(steganography_bp)

if __name__ == '__main__':
    app.run(debug=True)