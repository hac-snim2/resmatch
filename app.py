import difflib
import os
from flask import * # TODO: Specify imports

import data # Load data from CSV files in this repo


# Load data from CSV and JSON files
universities, uni_locations = data.load_uni_data()
orgs = data.load_orgs_data()
postcodes = data.load_postcode_data()


# Set up application.
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(24) # Needed for sessions.


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        close_matches = difflib.get_close_matches(request.form['university'], universities)
        if len(close_matches) == 0:
            return redirect(url_for('index'))
        best_guess = close_matches[0]
        flash('Searching for companies nere %s. Please be patient....' % best_guess)
        session['university'] = best_guess
        return redirect(url_for('results'))
    return """
<html>
  <head></head>
  <body>
     <h1>Search for active companies near your HEI</h1>
        <form action="" method="post">
            <p><strong>University or HEI:</strong> <input type=text name=university></p>
        </form>
  </body>
</html>
    """


@app.route('/results/')
def results():
    try:
        uni = session['university']
    except KeyError:
        return """<!DOCTYPE html>
<html>
<head><title>No university specified in search box</title></head>
<body>
<h1>You didn't give me a University to search for!</h1>
<p>Please go <a href="/">back</a> and try again.</p>
</body>
</html>
"""
    postcode = uni_locations[uni]['postcode']
    nearby = data.find_nearby_orgs(postcode, orgs, postcodes)
    results = {}
    results['university'] = uni
    results['long'] = uni_locations[uni]['long']
    results['lat'] = uni_locations[uni]['lat']
    results['postcode'] = uni_locations[uni]['postcode']
    companies = []
    for key in nearby:
        org = {}
        org['name'] = nearby[key][0][u'name']
        org['url'] = nearby[key][0][u'@attributes'][u'url']
        org['postcode'] = nearby[key][0][u'address'][u'postCode']
        lat, lng = data.get_latlong_from_postcode(org['postcode'], postcodes)
        org['lat'] = lat
        org['long'] = lng
        org['activity'] = '' # TODO - get this from somewhere
        companies.append(org)
    results['companies'] = companies
#    with open('justincase.json', 'w') as f:
#        json.dump(results, f)
    return """<html>
<head><title>Results for %s</title></head>
<body>
  <h1>Organisations near %s with prior research funding</h1>
  <p>
  <pre>
%s
  </pre>
  </p>
</body>
</html>
""" % (uni, uni, json.dumps(results))

