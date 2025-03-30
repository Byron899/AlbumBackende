from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

albums = [
    {"rank": 1, "title": "Thriller", "artist": "Michael Jackson"},
    {"rank": 2, "title": "Back in Black", "artist": "AC/DC"},
    {"rank": 3, "title": "The Dark Side of the Moon", "artist": "Pink Floyd"}
]

@app.route("/albums")
def get_albums():
    return jsonify(albums)

if __name__ == "__main__":
    app.run(debug=True)