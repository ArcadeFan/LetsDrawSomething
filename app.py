from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
import uuid
from datetime import datetime  

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

rooms = {} 


@app.route("/get_images/<room_code>")
def get_images(room_code):
    room_folder = os.path.join(UPLOAD_FOLDER, room_code)
    if not os.path.exists(room_folder):
        return jsonify([]) 

    images = sorted(os.listdir(room_folder), reverse=True)
    return jsonify(images)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_room", methods=["POST"])
def create_room():
    room_name = request.form.get("room_name", "Untitled")
    room_code = str(uuid.uuid4())[:6].upper()
    rooms[room_code] = {"name": room_name}
    

    room_folder = os.path.join(UPLOAD_FOLDER, room_code)
    os.makedirs(room_folder, exist_ok=True)

    return redirect(url_for('host', room_code=room_code))


@app.route("/join_room", methods=["POST"])
def join_room():
    room_code = request.form.get("room_code", "").upper()
    if room_code in rooms:
        return redirect(url_for('draw', room_code=room_code))
    return "Room not found", 404

@app.route("/host/<room_code>")
def host(room_code):
    room_folder = os.path.join(UPLOAD_FOLDER, room_code)
    if not os.path.exists(room_folder):
        return "Room not found", 404

    images = sorted(os.listdir(room_folder), reverse=True)
    return render_template("host.html", images=images, room_code=room_code, room_name=rooms[room_code]["name"])


@app.route("/draw/<room_code>")
def draw(room_code):
    room = rooms.get(room_code)
    if not room:
        return "Room not found", 404
    return render_template("draw.html", room_code=room_code, room_name=room["name"])

@app.route("/upload", methods=["POST"])
def upload():
    try:
        room_code = request.form.get("room_code")
        if room_code not in rooms:
            print(f"[ERROR] Invalid room code received: {room_code}")
            return "Invalid room", 400

        data = request.files['image']
        if not data:
            print("[ERROR] No image file received.")
            return "No image provided", 400

        room_folder = os.path.join(UPLOAD_FOLDER, room_code)
        os.makedirs(room_folder, exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        filepath = os.path.join(room_folder, filename)
        data.save(filepath)

        print(f"[INFO] Saved drawing to {filepath}")
        return "Uploaded"
    
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return "Upload failed", 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
