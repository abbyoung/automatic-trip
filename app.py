import os
import requests, json
from flask import Flask, render_template, redirect, request, session, url_for, flash

app = Flask(__name__)

@app.route("/")
def index():
    r = requests.get('https://api.automatic.com/v1/trips?per_page=10', headers={'Authorization': 'token '+os.environ["AUTOMATIC_KEY"]})
    recent_trips = r.json()
    return render_template("index.html", recent_trips=recent_trips)



if __name__ == "__main__":
    app.run(debug=True)