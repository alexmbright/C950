from datetime import datetime, timedelta, time
from package import Package
from hashmap import HashMap
import csv

# O(1)
address_updated_9 = False
# O(1)
_packages = HashMap()
# O(1)
_locations = []
# O(1)
_distances = []
# O(1)
_trucks = {}
# O(1)
_today = datetime.today()


# O(1)
def today():
    return _today


def deliver_packages(truck):
    start_time = truck.get_departure_time()
    packages = truck.get_packages()
    if not packages:
        return
    package_locations = {}
    locations = []
    # O(n)
    for pkg in packages:
        pkg_loc = int(get_location(get_package(pkg).address)['id'])
        if pkg_loc not in package_locations:
            package_locations[pkg_loc] = []
        package_locations[pkg_loc].append(pkg)
        locations.append(pkg_loc)
    current_location = 0
    visited_locations = [0]
    current_time = start_time
    total_miles = 0
    delivered = []

    # O(n)
    while len(delivered) < len(packages):
        global address_updated_9
        if not address_updated_9 and current_time >= today().replace(hour=10, minute=20):
            get_package(9).update_address('410 S State St', 'Salt Lake City', 'UT', '84111')
            address_updated_9 = True
        neighbors = get_available(current_location, locations, visited_locations)
        nearest = {}
        for neighbor in neighbors:
            if not nearest:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
                continue
            if neighbor['distance'] < nearest['distance']:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
        for pkg in package_locations.get(nearest['id']):
            nearest_package = get_package(pkg)
            delivered.append(nearest_package.get_id())
            nearest_package.set_delivered(True, current_time.replace(second=0))
        travel_minutes = (nearest['distance'] / truck.speed) * 60
        current_time += timedelta(minutes=travel_minutes)
        visited_locations.append(nearest['id'])
        current_location = nearest['id']
        total_miles += nearest['distance']

    # return to hub
    return_miles = get_distance(current_location, 0)
    total_miles += return_miles
    travel_minutes = (return_miles / truck.speed) * 60
    current_time += timedelta(minutes=travel_minutes)

    hours = int((total_miles // truck.speed))
    minutes = int(((total_miles / truck.speed) * 60) % 60)

    return {'delivered': delivered, 'miles': total_miles, 'end_time': current_time,
            'time_spent': f'{hours}h {minutes}m'}


# ------------------- PACKAGE METHODS -------------------
def scan_packages():
    with open('data/packages.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            deadline = line['deadline']
            if deadline == 'EOD':
                deadline = "11:59 PM"
            deadline_time = datetime.combine(today(), datetime.strptime(deadline, '%I:%M %p').time())
            package = Package(int(line['id']), line['address'], line['city'], line['state'], line['zip_code'],
                              deadline_time, int(line['weight']))
            _packages.put(package.package_id, package)


# O(1)
def get_all_packages():
    return _packages


# O(1)
def get_package(package_id):
    return _packages.get(package_id)


# O(n)
def get_packages_by_address(address):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.address == address:
            result.append(package)
    return result


# O(n)
def get_packages_by_deadline(deadline):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.deadline == deadline:
            result.append(package)
    return result


# O(n)
def get_packages_by_city(city):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.city == city:
            result.append(package)
    return result


# O(n)
def get_packages_by_zip(zip_code):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.zip_code == zip_code:
            result.append(package)
    return result


# O(n)
def get_packages_by_weight(weight):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.weight == weight:
            result.append(package)
    return result


# O(n)
def get_packages_by_status(status):
    result = []
    for i in range(1, 41):
        package = _packages.get(i)
        if package.status == status:
            result.append(package)
    return result


# ------------------- TRUCK METHODS -------------------

# O(1)
def put_truck(truck):
    _trucks[truck.id] = truck


# O(1)
def get_truck(truck_id):
    return _trucks[truck_id]


# O(1)
def get_all_trucks():
    return _trucks


# ------------------- LOCATION METHODS -------------------
def scan_locations():
    with open('data/locations.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            _locations.append({'id': line['id'], 'name': line['name'], 'address': line['address']})


# O(1)
def get_all_locations():
    return _locations


# O(n)
def get_location(address):
    for location in _locations:
        if location['address'] == address:
            return location


# ------------------- DISTANCE METHODS -------------------
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


# O(1)
def get_all_distances():
    return _distances


# O(n)
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


# O(n)
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


# O(1)
def get_distance(a, b):
    if a > b:
        return _distances[a][b]['distance']
    return _distances[b][a]['distance']
