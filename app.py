
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "albums.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/albums", methods=["GET", "POST"])
def albums():
    if request.method == "GET":
        albums = load_data()
        sort_key = request.args.get("sort", "average")
        order = request.args.get("order", "desc")
        albums.sort(key=lambda x: x.get(sort_key, 0), reverse=(order == "desc"))
        for i, a in enumerate(albums):
            a["rank"] = i + 1
        return jsonify(albums)
    else:
        albums = load_data()
        data = request.json
        total_score = sum(float(song["rating"]) for song in data["songs"])
        max_score = len(data["songs"]) * 10
        average = round(total_score / len(data["songs"]), 2)
        new_album = {
            "id": len(albums) + 1,
            **data,
            "total_score": total_score,
            "max_score": max_score,
            "average": average
        }
        albums.append(new_album)
        save_data(albums)
        return jsonify(new_album), 201

@app.route("/albums/<int:album_id>", methods=["DELETE", "PUT"])
def album_ops(album_id):
    albums = load_data()
    album = next((a for a in albums if a["id"] == album_id), None)
    if not album:
        return jsonify({"error": "Album not found"}), 404

    if request.method == "DELETE":
        albums = [a for a in albums if a["id"] != album_id]
        save_data(albums)
        return jsonify({"success": True})

    if request.method == "PUT":
        data = request.json
        album.update(data)
        total_score = sum(float(song["rating"]) for song in data["songs"])
        max_score = len(data["songs"]) * 10
        average = round(total_score / len(data["songs"]), 2)
        album.update({
            "total_score": total_score,
            "max_score": max_score,
            "average": average,
        })
        save_data(albums)
        return jsonify(album)

if __name__ == "__main__":
    app.run(debug=True)
