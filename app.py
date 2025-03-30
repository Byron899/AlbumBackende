from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "albums.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        albums = json.load(f)
else:
    albums = []

@app.route("/albums", methods=["GET"])
def get_albums():
    sort_key = request.args.get("sort", "average")
    reverse = request.args.get("order", "desc") == "desc"
    sorted_albums = sorted(albums, key=lambda x: x.get(sort_key, 0), reverse=reverse)
    for idx, album in enumerate(sorted_albums):
        album["rank"] = idx + 1
    return jsonify(sorted_albums)

@app.route("/albums", methods=["POST"])
def add_album():
    data = request.json
    title = data.get("title")
    artist = data.get("artist")
    album_type = data.get("type", "Album")
    songs = data.get("songs", [])
    if not title or not artist or not songs:
        return jsonify({"error": "Missing fields"}), 400

    total_score = sum(float(song.get("rating", 0)) for song in songs)
    avg_score = round(total_score / len(songs), 2)
    album_id = max([a["id"] for a in albums], default=0) + 1

    album = {
        "id": album_id,
        "title": title,
        "artist": artist,
        "type": album_type,
        "songs": songs,
        "average": avg_score,
        "total_score": total_score,
        "max_score": len(songs) * 10,
    }
    albums.append(album)
    save_albums()
    return jsonify(album), 201

@app.route("/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    data = request.json
    for album in albums:
        if album["id"] == album_id:
            album.update({
                "title": data.get("title", album["title"]),
                "artist": data.get("artist", album["artist"]),
                "type": data.get("type", album["type"]),
                "songs": data.get("songs", album["songs"])
            })
            total_score = sum(float(song.get("rating", 0)) for song in album["songs"])
            avg_score = round(total_score / len(album["songs"]), 2)
            album["total_score"] = total_score
            album["average"] = avg_score
            album["max_score"] = len(album["songs"]) * 10
            save_albums()
            return jsonify(album)
    return jsonify({"error": "Album not found"}), 404

@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    global albums
    albums = [a for a in albums if a["id"] != album_id]
    save_albums()
    return jsonify({"message": "Deleted"}), 200

def save_albums():
    with open(DB_FILE, "w") as f:
        json.dump(albums, f, indent=2)

if __name__ == "__main__":
    app.run()