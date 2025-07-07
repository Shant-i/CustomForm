from flask import Flask, request, redirect, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)
SECRET_TOKEN = "mysecret"

@app.route("/")
def form():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return "Unauthorized", 403
    return open("form.html").read()

@app.route("/submit", methods=["POST"])
def submit():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return "Unauthorized", 403

    name = request.form["name"]
    age = request.form["age"]
    color = request.form["color"]
    email = request.form["email"]
    message = request.form["message"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("responses.csv", "a", encoding="utf-8") as f:
        f.write(f"{time},{name},{age},{color},{email},{message}\n")

    return redirect(f"/?token={SECRET_TOKEN}")

@app.route("/responses")
def responses():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return "Unauthorized", 403

    try:
        with open("responses.csv", "r", encoding="utf-8") as f:
            return "<pre>" + f.read() + "</pre>"
    except FileNotFoundError:
        return "No responses yet."

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
