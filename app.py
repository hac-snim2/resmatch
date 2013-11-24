import os
from flask import * # TODO: Specify imports

import data # Load data from CSV files in this repo

# Load data from CSV files
universities, uni_locations = data.load_uni_data()

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(24) # Needed for sessions.


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flash('Searching for companies nere %s. Please be patient....' % request.form['university'])
        session['university'] = request.form['university']
        return redirect(url_for('results'))
    return '''
<html>
  <head></head>
  <body>
     <h1>Search for active companies near your HEI</h1>
        <form action="" method="post">
            <p><strong>University or HEI:</strong> <input type=text name=university></p>
        </form>
  </body>
</html>
    '''

@app.route('/results/')
def results():
    return 'Hello world!\n'
