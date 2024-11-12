from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/spotify/login")
def spotify_login():
    return "<p>Spotify Login</p>"

if __name__ == "__main__":
    app.run() 