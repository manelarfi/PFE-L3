from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Hello, Flask! This is a console log.")  # This prints to the server console
    return "Check your console!"

if __name__ == "__main__":
    app.run(debug=True)
