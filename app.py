from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

albums = []
album_id_counter = 1

@app.route("/albums", methods=["GET"])
def get_albums():
    sorted_albums = sorted(albums, key=lambda x: x.get("average", 0), reverse=True)
    for idx, album in enumerate(sorted_albums):
        album["rank"] = idx + 1
    return jsonify(sorted_albums)

@app.route("/albums", methods=["POST"])
def add_album():
    global album_id_counter
    data = request.json
    title = data.get("title")
    artist = data.get("artist")
    album_type = data.get("type", "Album")
    songs = data.get("songs", [])

    if not title or not artist or not songs:
        return jsonify({"error": "Missing fields"}), 400

    total_score = sum(float(song.get("rating", 0)) for song in songs)
    avg_score = round(total_score / len(songs), 2)

    album = {
        "id": album_id_counter,
        "title": title,
        "artist": artist,
        "type": album_type,
        "songs": songs,
        "average": avg_score,
        "total_score": total_score,
        "max_score": len(songs) * 10,
    }
    album_id_counter += 1
    albums.append(album)
    return jsonify(album), 201