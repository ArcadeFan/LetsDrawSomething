from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for rooms
rooms = {}  # key: room_code, value: dict with room info (e.g. 'name')

# Landing page: shows the room creation form (index.html)
@app.route("/")
def index():
    return render_template("index.html")

# Route to create a new room from the form submission in index.html
@app.route("/create_room", methods=["POST"])
def create_room():
    # Grab the host's name and the room name from the form
    username = request.form.get("username", "Host")
    room_name = request.form.get("room_name", "Untitled Room")
    # Generate a short room code (e.g. "A1B2C3")
    room_code = str(uuid.uuid4())[:6].upper()
    # Save the room info in our in-memory store
    rooms[room_code] = {"name": room_name, "created_by": username}
    # Redirect to the drawing page for that room
    return redirect(url_for("draw", room_code=room_code))

# Updated draw route to include the room code in the URL
@app.route("/draw/<room_code>")
def draw(room_code):
    if room_code in rooms:
        room_name = rooms[room_code]["name"]
        # Pass room_code and room_name into draw.html
        return render_template("draw.html", room_code=room_code, room_name=room_name)
    return "Room not found", 404

# Optional: You can create a room-specific host view as well.
# This example will serve host view for a given room, though you can expand on it.
@app.route("/host/<room_code>")
def host(room_code):
    if room_code in rooms:
        # For now, we're still listing all images from static/uploads,
        # but you might later separate by room (e.g. store uploads under uploads/<room_code>/).
        images = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
        return render_template("host.html", images=images, room_code=room_code, room_name=rooms[room_code]["name"])
    return "Room not found", 404

# Existing upload route remains unchanged
@app.route("/upload", methods=["POST"])
def upload():
    data = request.files.get("image")
    if data:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        data.save(filepath)
        return "Uploaded"
    return "No image", 400

if __name__ == "__main__":
    # Bind to the port provided by the environment (for Render) and host 0.0.0.0.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
