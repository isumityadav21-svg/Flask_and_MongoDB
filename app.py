from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["FlaskDB"]
collection = db["submissions"]


# Task 1: JSON API Route
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return data

    except Exception as e:
        return {"error": str(e)}, 500


# Frontend Form
@app.route("/", methods=["GET", "POST"])
def index():

    error = None

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        try:

            if not name or not email or not message:
                error = "All fields are required."
                return render_template("index.html", error=error)

            submission = {
                "name": name,
                "email": email,
                "message": message
            }

            collection.insert_one(submission)

            # Success -> redirect
            return redirect(url_for("success"))

        except Exception as e:

            # Error -> same page
            error = f"Database Error: {str(e)}"

            return render_template("index.html", error=error)

    return render_template("index.html", error=error)


# Success Page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
