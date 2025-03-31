from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'albums.json'

def load_albums():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_albums(albums):
    with open(DATA_FILE, 'w') as f:
        json.dump(albums, f, indent=2)

@app.route("/albums", methods=["GET"])
def get_albums():
    return jsonify(load_albums())

@app.route("/albums", methods=["POST"])
def add_album():
    albums = load_albums()
    new_album = request.json
    new_album["id"] = max([a["id"] for a in albums], default=0) + 1
    albums.append(new_album)
    save_albums(albums)
    return jsonify({"success": True}), 201

@app.route("/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    albums = load_albums()
    for i, album in enumerate(albums):
        if album["id"] == album_id:
            albums[i] = {**request.json, "id": album_id}
            save_albums(albums)
            return jsonify({"success": True})
    return jsonify({"error": "Album not found"}), 404

@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    albums = load_albums()
    albums = [a for a in albums if a["id"] != album_id]
    save_albums(albums)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
