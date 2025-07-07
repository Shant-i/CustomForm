import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16 MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.args.get("token") != "mysecret":
        return "Unauthorized", 403

    # Get form fields
    date = request.form.get("date")
    mood = request.form.get("mood")
    elaboration = request.form.get("Elaboration")
    song = request.form.get("Song you're listening to right now")
    descriptions = request.form.getlist("image_descriptions[]")

    # Process file uploads
    uploaded_images = []
    if 'images[]' in request.files:
        files = request.files.getlist('images[]')
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                uploaded_images.append({
                    "filename": filename,
                    "description": descriptions[i] if i < len(descriptions) else ""
                })

    # You can optionally log or save the submission here
    print("Date:", date)
    print("Mood:", mood)
    print("Elaboration:", elaboration)
    print("Song:", song)
    print("Images:", uploaded_images)

    return render_template("thankyou.html", images=uploaded_images)


# Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
