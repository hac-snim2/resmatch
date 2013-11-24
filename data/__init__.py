import csv
import json
import requests

from math import sqrt

_UNI_FILE = 'data/uk-uni-locations.csv'

_ORGS_FILE = 'data/orgs.json'

_PC_FILE = 'data/postcodes.csv'

MIN_DIST = 50


def find_nearby_orgs(postcode, orgs, postcodes):
    """TODO: Maybe better to hold the orgs data here?
    """
    nearby = {}
    origin = postcode.replace(' ', '')
    for pc in orgs.keys():
        dist = distance_between_postcodes(origin, pc, postcodes) 
        if dist is None: continue
        if dist < MIN_DIST:
            nearby[pc] = orgs[pc]
    return nearby


def load_orgs_data():
    with open(_ORGS_FILE, 'r') as f:
        data = json.load(f)
        return data
    return dict()


def load_postcode_data():
    """Load CSV file of postcode data into memory.
    Return in JSON.
    """
    postcodes = dict()
    with open(_PC_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'postcode' or len(row) != 9: continue
            postcodes[row[0].replace(' ', '')] = {'postcode' : row[0],
                                                  'eastings' : row[1],
                                                  'northings' : row[2],
                                                  'latitude' : row[3],
                                                  'longitude' : row[4],
                                                  'town' : row[5],
                                                  'region' : row[6]
                                                  }
    return postcodes


def load_uni_data():
    """Load CSV file of university locations into memory.
    Return a dict.
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


def distance_between_postcodes(pc1, pc2, postcodes):
   try:
        e1 = postcodes[pc1.replace(' ', '')]['eastings']
        n1 = postcodes[pc1.replace(' ', '')]['northings']
        e2 = postcodes[pc2.replace(' ', '')]['eastings']
        n2 = postcodes[pc2.replace(' ', '')]['northings']
        return sqrt(pow((e2 - e1), 2) + pow((n2 - n1), 2))
    except KeyError:
        return None
