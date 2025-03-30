
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from uuid import uuid4

app = Flask(__name__)
CORS(app)

DB_FILE = "albums.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/albums", methods=["GET"])
def get_albums():
    albums = load_data()
    return jsonify(albums)

@app.route("/albums", methods=["POST"])
def add_album():
    album = request.json
    album["id"] = str(uuid4())
    albums = load_data()
    albums.append(album)
    save_data(albums)
    return jsonify({"message": "Album added", "id": album["id"]}), 201

@app.route("/albums/<album_id>", methods=["DELETE"])
def delete_album(album_id):
    albums = load_data()
    albums = [a for a in albums if a["id"] != album_id]
    save_data(albums)
    return jsonify({"message": "Album deleted"})

if __name__ == "__main__":
    app.run(debug=True)
