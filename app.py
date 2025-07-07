from flask import Flask, render_template, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def form():
    return render_template("form.html")  # Your HTML file should be named 'form.html' and placed in the 'templates' folder

@app.route("/submit", methods=["POST"])
def submit():
    date = request.form.get("date")
    mood = request.form.get("mood")
    elaboration = request.form.get("Elaboration")
    song = request.form.get("Song you're listening to right now")

    photos = []
    for i in range(1, 4):
        file = request.files.get(f"photo{i}")
        desc = request.form.get(f"desc{i}")
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            photos.append({"filename": filename, "description": desc})

    # Here you can save the data and images to a database or a file

    return redirect("/thankyou")

@app.route("/thankyou")
def thank_you():
    return "<h1 style='text-align:center;'>Thank you for your submission! :)</h1>"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
