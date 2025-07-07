@app.route("/submit", methods=["POST"])
def submit():
    if request.args.get("token") != "mysecret":
        return "Unauthorized", 403

    # Get form data
    date = request.form.get("date")
    mood = request.form.get("mood")
    elaboration = request.form.get("Elaboration")
    song = request.form.get("Song you're listening to right now")

    # Handle multiple uploaded files
    uploaded_images = []
    if 'images' in request.files:
        images = request.files.getlist("images")
        descriptions = request.form.getlist("image_descriptions")

        for i, image in enumerate(images):
            if image.filename != "":
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                uploaded_images.append({
                    'filename': filename,
                    'description': descriptions[i] if i < len(descriptions) else ""
                })

    # Save to CSV
    with open('responses.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        row = [datetime.now().isoformat(), date, mood, elaboration, song]
        for img in uploaded_images:
            row.append(img['filename'])
            row.append(img['description'])
        writer.writerow(row)

    # Email notification
    send_email_notification(date, mood, elaboration, song)

    return render_template("thankyou.html", images=uploaded_images)
