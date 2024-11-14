from flask import Flask, jsonify, request
import spotify

app = Flask(__name__)

headers = spotify.Authenticate()

@app.route("/")
def home():
    return "<p>Spotify Login</p>"

@app.route("/spotify")
def spotify_playlist():
    return jsonify(spotify.get_playlist(headers))

if __name__ == "__main__":
    app.run() 