import csv
import package

_locations = []
_distances = []
_visited = []


def scan_locations():
    with open('data/locations.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            _locations.append({'id': line['id'], 'name': line['name'], 'address': line['address']})


def get_all_locations():
    return _locations


def get_location(address):
    for location in _locations:
        if location['address'] == address:
            return location


def scan_distances():
    with open('data/distances.csv') as file:
        reader = csv.reader(file)

        i = 0
        for line in reader:
            _curr_distances = []
            for j in range(len(line)):
                if line[j]:
                    _curr_distances.append({'id': j, 'distance': float(line[j])})
            _distances.append(_curr_distances)
            i += 1


def get_all_distances():
    return _distances


def get_all_available(a, visited):
    if visited is None:
        visited = []
    _available = []
    for i in range(len(_locations)):
        if i >= len(_distances):
            continue
        if i != a and i not in visited:
            _available.append({'id': i, 'distance': get_distance(i, a)})
    return _available


def get_available(a, locations, visited):
    if visited is None:
        visited = []
    _available = []
    for i in range(len(_locations)):
        if i >= len(_distances):
            continue
        if i in locations and i != a and i not in visited:
            _available.append({'id': i, 'distance': get_distance(i, a)})
    return _available


def get_distance(a, b):
    if a > b:
        return _distances[a][b]['distance']
    return _distances[b][a]['distance']

