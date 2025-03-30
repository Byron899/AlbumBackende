from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
import os

app = Flask(__name__)
CORS(app)

STORAGE_FILE = "albums.json"

def load_albums():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return []

def save_albums(albums):
    with open(STORAGE_FILE, "w") as f:
        json.dump(albums, f, indent=2)

@app.route("/albums", methods=["GET"])
def get_albums():
    sort_key = request.args.get("sort", "average")
    sort_order = request.args.get("order", "desc")
    albums = load_albums()
    for album in albums:
        ratings = [float(song["rating"]) for song in album["songs"] if song.get("rating")]
        album["total_score"] = sum(ratings)
        album["max_score"] = len(ratings) * 10
        album["average"] = round(album["total_score"] / len(ratings), 2) if ratings else 0
    albums.sort(key=lambda x: x.get(sort_key, 0), reverse=(sort_order == "desc"))
    for i, album in enumerate(albums, 1):
        album["rank"] = i
    return jsonify(albums)

@app.route("/albums", methods=["POST"])
def add_album():
    album = request.json
    album["id"] = str(uuid.uuid4())
    albums = load_albums()
    albums.append(album)
    save_albums(albums)
    return jsonify({"message": "Album added", "id": album["id"]}), 201

@app.route("/albums/<album_id>", methods=["PUT"])
def update_album(album_id):
    update = request.json
    albums = load_albums()
    for i, album in enumerate(albums):
        if album["id"] == album_id:
            albums[i] = {**album, **update, "id": album_id}
            break
    save_albums(albums)
    return jsonify({"message": "Album updated"})

@app.route("/albums/<album_id>", methods=["DELETE"])
def delete_album(album_id):
    albums = load_albums()
    albums = [a for a in albums if a["id"] != album_id]
    save_albums(albums)
    return jsonify({"message": "Album deleted"})

if __name__ == "__main__":
    app.run(debug=True)