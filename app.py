
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

albums = []

@app.route("/albums", methods=["GET", "POST"])
def handle_albums():
    if request.method == "POST":
        data = request.json
        album_id = str(uuid.uuid4())
        total_score = sum(float(song["rating"]) for song in data["songs"])
        max_score = len(data["songs"]) * 10
        average = round(total_score / len(data["songs"]), 2)
        album = {
            "id": album_id,
            "title": data["title"],
            "artist": data["artist"],
            "type": data.get("type", "Album"),
            "songs": data["songs"],
            "total_score": total_score,
            "max_score": max_score,
            "average": average
        }
        albums.append(album)
        return jsonify(album), 201
    else:
        sort_key = request.args.get("sort", "average")
        order = request.args.get("order", "desc")
        sorted_albums = sorted(albums, key=lambda x: x.get(sort_key, 0), reverse=(order == "desc"))
        for i, album in enumerate(sorted_albums, 1):
            album["rank"] = i
        return jsonify(sorted_albums)

@app.route("/albums/<album_id>", methods=["PUT", "DELETE"])
def modify_album(album_id):
    global albums
    if request.method == "PUT":
        data = request.json
        for album in albums:
            if album["id"] == album_id:
                album.update({
                    "title": data["title"],
                    "artist": data["artist"],
                    "type": data.get("type", "Album"),
                    "songs": data["songs"]
                })
                total_score = sum(float(song["rating"]) for song in album["songs"])
                max_score = len(album["songs"]) * 10
                album["total_score"] = total_score
                album["max_score"] = max_score
                album["average"] = round(total_score / len(album["songs"]), 2)
                return jsonify(album)
        return jsonify({"error": "Not found"}), 404
    elif request.method == "DELETE":
        albums = [a for a in albums if a["id"] != album_id]
        return "", 204
