from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load .env if not in production

app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.snapnote

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        if entry_content:  # Basic validation
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            db.entries.insert_one({"content": entry_content, "date": formatted_date})
        return redirect(url_for("home"))

    entries = [
        (e["content"], e["date"], datetime.datetime.strptime(e["date"], "%Y-%m-%d").strftime("%b %d"))
        for e in db.entries.find({})
    ]
    return render_template("home.html", entries=entries)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
