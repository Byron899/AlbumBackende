
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

albums = []

@app.route("/albums", methods=["GET"])
def get_albums():
    sort_key = request.args.get("sort", "average")
    order = request.args.get("order", "desc")

    sorted_albums = sorted(albums, key=lambda a: a.get(sort_key, 0), reverse=(order == "desc"))
    for i, a in enumerate(sorted_albums):
        a["rank"] = i + 1
    return jsonify(sorted_albums)

@app.route("/albums", methods=["POST"])
def add_album():
    data = request.get_json()
    if not data or "title" not in data or "artist" not in data or "songs" not in data:
        return jsonify({"error": "Invalid data"}), 400

    ratings = [float(s["rating"]) for s in data["songs"] if "rating" in s]
    total_score = sum(ratings)
    max_score = len(ratings) * 10
    average = round(total_score / len(ratings), 2) if ratings else 0

    album = {
        "id": str(uuid.uuid4()),
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

@app.route("/albums/<album_id>", methods=["PUT"])
def update_album(album_id):
    data = request.get_json()
    for i, album in enumerate(albums):
        if album["id"] == album_id:
            ratings = [float(s["rating"]) for s in data["songs"] if "rating" in s]
            total_score = sum(ratings)
            max_score = len(ratings) * 10
            average = round(total_score / len(ratings), 2) if ratings else 0

            updated_album = {
                "id": album_id,
                "title": data["title"],
                "artist": data["artist"],
                "type": data.get("type", "Album"),
                "songs": data["songs"],
                "total_score": total_score,
                "max_score": max_score,
                "average": average
            }
            albums[i] = updated_album
            return jsonify(updated_album)
    return jsonify({"error": "Album not found"}), 404

@app.route("/albums/<album_id>", methods=["DELETE"])
def delete_album(album_id):
    global albums
    albums = [a for a in albums if a["id"] != album_id]
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
