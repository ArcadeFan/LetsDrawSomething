from flask import Flask, render_template, request, redirect
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return redirect("/draw")

@app.route("/draw")
def draw():
    return render_template("draw.html")

@app.route("/host")
def host():
    images = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    return render_template("host.html", images=images)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.files['image']
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    data.save(filepath)
    return "Uploaded"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
