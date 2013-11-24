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
        best_guess = difflib.get_close_matches(request.form['university'], universities)[0]
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
    print 'DEBUG %s' % uni
    postcode = uni_locations[uni]['postcode']
    nearby = data.find_nearby_orgs(postcode, orgs, postcodes)
    for key in nearby: print nearby[key] + '\n\n'
    results = {}
    #    results['university'] = uni
#    results['long'] = uni_locations[uni]['long']
#    results['lat'] = uni_locations[uni]['lat']
#    results['postcode'] = uni_locations[uni]['postcode']
#    companies = []
#    for co in nearby:
#        org = {}
#        org['name'] = co[
#    return 
    return 'You are searching for companies around %s\n' % session['university']
