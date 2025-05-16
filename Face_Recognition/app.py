from flask import Flask, request, render_template, send_file
from recognizer import load_known_faces, recognize_faces
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

# Load data at startup
known_encodings, known_names = load_known_faces()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        img_file = request.files["image"]
        if not img_file:
            return "No file uploaded", 400
        
        # Save upload
        file_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
        img_file.save(file_path)

        # Prepare result path
        result_filename = f"{uuid.uuid4()}.jpg"
        result_path = os.path.join(RESULT_FOLDER, result_filename)

        # Run recognition
        recognize_faces(file_path, known_encodings, known_names, result_path)

        return send_file(result_path, mimetype="image/jpeg")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)