import csv
import json
import requests

from math import sqrt

_PC_FINDER = 'http://uk-postcodes.com/'

_UNI_FILE = 'data/uk-uni-locations.csv'

_ORGS_FILE = 'data/orgs.json'

MIN_DIST = 50


def find_nearby_orgs(postcode, orgs):
    """TODO: Maybe better to hold the orgs data here?
    """
    nearby = {}
    for pc in orgs.keys():
        if distance_between_postcodes(postcode, pc) < MIN_DIST:
            nearby[pc] = orgs[pc]
    return nearby


def load_orgs_data():
    with open(_UNI_FILE, 'r') as f:
        data = json.load(f)
        return data
    return dict()


def load_uni_data():
    """Load CSV file of university locations into memory.
    Return in JSON.
    """
    universities = []
    uni_locations = {}
    with open(_UNI_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'name' or len(row) != 4: continue
            universities.append(row[0])
            uni_locations[row[0]] = { 'postcode' : row[1],
                                      'lat'      : row[2],
                                      'long'     : row[3]
                                    }
    return universities, uni_locations


def postcode_to_long_lat(pc):
    """TODO: Sort out exception handling
    """
    postcode = pc.replace(' ', '')
    url = _PC_FINDER + '/postcode/' + postcode + '.' + fmt
    r = requests.get(url)
    if r.status_code != 200: return 0, 0
    content = r.content
    result = {}
    result['lat'] = content['geo']['lat']
    result['lang'] = content['geo']['lng']
    return result 


def distance_between_postcodes(pc1, pc2):
    # Grab data for pc1
    postcode1 = pc1.replace(' ', '')
    url = _PC_FINDER + '/postcode/' + postcode1 + '.json'
    r1 = requests.get(url)
    if r1.status_code != 200: return 0
    content1 = r1.content
    # Grab data for pc2
    postcode2 = pc2.replace(' ', '')
    url = _PC_FINDER + '/postcode/' + postcode2 + '.json'
    r2 = requests.get(url)
    if r2.status_code != 200: return 0
    content2 = r2.content
    # Get distance
    e1, n1 = content1['geo']['easting'], content1['geo']['northing']
    e2, n2 = content2['geo']['easting'], content2['geo']['northing']
    return math.sqrt(pow((e2 - e1), 2) + pow((n2 - n1), 2))
