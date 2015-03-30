# -*- coding: utf-8 -*-

import os
import requests, json, datetime
from flask import Flask, render_template, redirect, request, session, url_for, flash



app = Flask(__name__)

# value = datetime.datetime.fromtimestamp(timestamp)
# print(value.strftime('%Y-%m-%d %H:%M:%S'))

@app.route("/")
def index():
    # Get recent 10 trips from Automatic
    # Using sandbox Automatic user
    try:
        r = requests.get('https://api.automatic.com/v1/trips?per_page=10', headers={'Authorization': 'token '+os.environ["AUTOMATIC_KEY"]})
        recent_trips = r.json()
    except Exception, e:
        return 'This is where the error handling would go.'

    # Get dates of trips
    for i in range(len(recent_trips)):
        start_time = recent_trips[i]['start_time']
        recent_trips[i]['start_time'] = (datetime.datetime.fromtimestamp(start_time/1000)).strftime('%a, %b. %-d, %Y %I:%M %p')

    # Get friends from Venmo
    # Using sandbox api with personal Venmo ID. Add your own to see your friends!
    try:
        friends = requests.get('https://sandbox-api.venmo.com/v1/users/974538061905920884/friends?access_token='+os.environ["VENMO_KEY"]+'&limit=1000')
        friends = friends.json()['data']
    except Exception, e:
        return 'This is where the error handling would go.'
    
    return render_template("index.html", recent_trips=recent_trips, friends=friends, venmo_key=os.environ['VENMO_KEY'], map_key=os.environ['MAP_KEY'])

@app.route("/payment", methods=["POST"])
def payment(): 

    trip_id = request.form['trip_id']
       
    # If using the real Venmo API, the following data would be passed
    if os.environ.get('CONFIG') == 'production':
        data = {'access_token': os.environ['VENMO_KEY'], 'user_id': request.form['user_id'], 'amount': "-"+(request.form['price']), 'note': 'Gas charge'}
        r = requests.post('https://api.venmo.com/v1/payments?access_token=', data=data)
    
    # But we have to hard-code sandbox user details to comply with sandbox API
    else:
        data = {'access_token': os.environ['VENMO_KEY'], 'user_id': '145434160922624933', 'amount': '-0.20', 'note': 'Gas charge'}
        r = requests.post('https://sandbox-api.venmo.com/v1/payments?access_token=', data=data)
    
    payment = json.dumps(r.json())
    return payment



if __name__ == "__main__":
    app.run(debug=True)