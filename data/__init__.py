import csv
import json

_UNI_FILE = 'data/uk-uni-locations.csv'


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
