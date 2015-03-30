# -*- coding: utf-8 -*-

import os
import requests, json
from flask import Flask, render_template, redirect, request, session, url_for, flash



app = Flask(__name__)



@app.route("/")
def index():
    # Get recent 10 trips from Automatic
    # Using sandbox Automatic user
    r = requests.get('https://api.automatic.com/v1/trips?per_page=10', headers={'Authorization': 'token '+os.environ["AUTOMATIC_KEY"]})
    recent_trips = r.json()
   

    # Get friends from Venmo
    # Using sandbox api with personal Venmo ID. Add your own to see your friends!
    friends = requests.get('https://sandbox-api.venmo.com/v1/users/974538061905920884/friends?access_token='+os.environ["VENMO_KEY"]+'&limit=1000')
    friends = friends.json()['data']

    return render_template("index.html", recent_trips=recent_trips, friends=friends, venmo_key=os.environ['VENMO_KEY'])

@app.route("/payment", methods=["POST"])
def payment(): 
    trip_id = request.form['trip_id']
    # If using the real Venmo API, the following data would be passed
    # data = {'access_token': os.environ['VENMO_KEY'], 'user_id': request.form['user_id'], 'amount': '-0.20', 'note': 'Gas charge'}
    # But we have to hard-code sandbox user details to comply with sandbox API
    data = {'access_token': os.environ['VENMO_KEY'], 'user_id': '145434160922624933', 'amount': '-0.20', 'note': 'Gas charge'}
    r = requests.post('https://sandbox-api.venmo.com/v1/payments?access_token=', data=data)
    payment = json.dumps(r.json())
    return payment



if __name__ == "__main__":
    app.run(debug=True)