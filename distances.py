import csv

_locations = []


def scan_locations():
    with open('data/locations.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            _locations.append({'id': line['id'], 'name': line['name'], 'address': line['address']})


def get_all_locations():
    return _locations


def get_location(loc_id):
    for location in _locations:
        if location['id'] == loc_id:
            return location