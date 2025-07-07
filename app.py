from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Setup for uploads
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route: Form page
@app.route("/")
def form():
    token = request.args.get("token")
    if token != "mysecret":
        return "Unauthorized", 403
    return render_template("form.html")

# Route: Handle form submission
@app.route("/submit", methods=["POST"])
def submit():
    if request.args.get("token") != "mysecret":
        return "Unauthorized", 403

    # Get form fields
    date = request.form.get("date")
    mood = request.form.get("mood")
    elaboration = request.form.get("Elaboration")
    song = request.form.get("Song you're listening to right now")

    # Save uploaded images
    uploaded_images = []
    if 'images' in request.files:
        images = request.files.getlist("images")
        descriptions = request.form.getlist("image_descriptions")

        for i, image in enumerate(images):
            if image and image.filename:
                filename = secure_filename(f"{datetime.now().timestamp()}_{image.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                desc = descriptions[i] if i < len(descriptions) else ""
                uploaded_images.append((filename, desc))

    # Save to CSV
    row = [datetime.now().isoformat(), date, mood, elaboration, song]
    for fname, desc in uploaded_images:
        row.extend([fname, desc])

    with open('responses.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    # Send email notification
    send_email_notification(date, mood, elaboration, song)

    return render_template("thankyou.html", images=uploaded_images)


# Route: View responses
@app.route("/responses")
def view_responses():
    token = request.args.get("token")
    if token != "1710":
        return "Unauthorized", 403

    data = []
    if os.path.exists("responses.csv"):
        with open("responses.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)

    return render_template("responses.html", responses=data)


# Route: Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Email function
def send_email_notification(date, mood, elaboration, song):
    msg = EmailMessage()
    msg['Subject'] = f'📝 New Form Submission on {date}'
    msg['From'] = 'sourabh.ic.kharche@gmail.com'
    msg['To'] = 'sourabh.ic.kharche@gmail.com'  # CHANGE THIS

    msg.set_content(f"""
New Form Submission Received:

Date: {date}
Mood: {mood}
Elaboration: {elaboration}
Song: {song}
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('sourabh.ic.kharche@gmail.com', 'ymvu pgyf ykem ecga')  # CHANGE THIS
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


# App entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
