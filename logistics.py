import copy
from datetime import datetime, timedelta, time
from package import Package
from hashmap import HashMap
import csv

# Boolean used to prevent updating package 9's address more than once during the optimization algorithm
_address_updated_9 = False

# Will point to copied instance of package 9 with old address after all deliveries are completed.
# This allows the old address to be used in lookups performed before 10:20 am.
_package_9_old = None

# Create appropriate data structures for the program
_packages = HashMap(71)
_locations = []
_distances = []
_trucks = {}

"""
Datetime object used in creating, comparing, and manipulating
all relevant datetime objects throughout the program
"""
today = datetime.combine(datetime.today(), time(0))


# Space-time complexity analyzed inside function
def deliver_packages(truck):
    start_time = truck.get_departure_time()
    packages = truck.get_packages()

    # Cancel package delivery if package list is empty
    if not packages:
        return

    # Create list of all package locations for use in nearest neighbor algorithm
    package_locations = {}
    locations = []
    for pkg in packages:
        pkg_loc = int(get_location(get_package(pkg).address)['id'])
        if pkg_loc not in package_locations:
            package_locations[pkg_loc] = []
        package_locations[pkg_loc].append(pkg)
        locations.append(pkg_loc)

    # Create appropriate variables and data structures for use in algorithm
    current_location = 0
    visited_locations = [0]
    current_time = start_time
    total_miles = 0
    delivered = []

    """
    Nearest Neighbor Algorithm
    
    Time: 
    Space: 
    """
    while len(delivered) < len(packages):

        # If current delivery time is on or after 10:20 am, update package 9's address.
        # Makes use of the boolean variable 'address_updated_9' as noted earlier.
        global _address_updated_9
        if not _address_updated_9 and current_time >= today.replace(hour=10, minute=20):
            get_package(9).update_address('410 S State St', 'Salt Lake City', 'UT', '84111')
            _address_updated_9 = True

        # Generate dictionary list of all unvisited neighbors
        neighbors = get_available(current_location, locations, visited_locations)

        # Find nearest neighbor (location with the shortest distance)
        nearest = {}
        for neighbor in neighbors:
            if not nearest:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
                continue
            if neighbor['distance'] < nearest['distance']:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}

        # Calculate delivery distance and time
        travel_minutes = (nearest['distance'] / truck.speed) * 60
        current_time += timedelta(minutes=travel_minutes)
        total_miles += nearest['distance']

        # Deliver and update all packages found at current delivery location
        for pkg in package_locations.get(nearest['id']):
            nearest_package = get_package(pkg)
            delivered.append(nearest_package.get_id())
            nearest_package.set_delivered(True, current_time.replace(second=0))

        # Mark current location as visited
        current_location = nearest['id']
        visited_locations.append(current_location)

    # Return truck to hub after all deliveries are complete
    return_miles = get_distance(current_location, 0)
    total_miles += return_miles
    travel_minutes = (return_miles / truck.speed) * 60
    current_time += timedelta(minutes=travel_minutes)

    # Calculate total time traveled using miles traveled and truck speed
    hours = int((total_miles // truck.speed))
    minutes = int(((total_miles / truck.speed) * 60) % 60)

    # Finally, set the delivery metrics for the truck
    truck.set_metrics({'delivered': delivered, 'miles': total_miles, 'end_time': current_time,
                       'time_spent': f'{hours}h {minutes}m'})


"""
------------------------
    PACKAGE METHODS
------------------------
"""


# Time: O(n) - Space: O(n)
def scan_packages():
    with open('data/packages.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            deadline = line['deadline']
            if deadline == 'EOD':
                deadline = "5:00 PM"
            deadline_time = datetime.combine(today, datetime.strptime(deadline, '%I:%M %p').time())
            package = Package(int(line['id']), line['address'], line['city'], line['state'], line['zip_code'],
                              deadline_time, int(line['weight']))
            _packages.put(package.package_id, package)


# Time: O(1) - Space: O(1)
def get_all_packages():
    return _packages


# Time: O(n) -- HashMap get() function = O(n)
# Space: O(1)
def get_package(package_id):
    return _packages.get(package_id)


# Time: O(n)
def get_packages_by_address(address, time_req):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.get_id() == 9 and time_req < today.replace(hour=10, minute=20):
            package = _package_9_old
        if package.address.lower() == address.lower():
            result.append(package)
    return result


# O(n)
def get_packages_by_deadline(deadline):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.deadline == deadline:
            result.append(package)
    return result


# O(n)
def get_packages_by_city(city):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.city.lower() == city.lower():
            result.append(package)
    return result


# O(n)
def get_packages_by_zip(zip_code, time_req):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.get_id() == 9 and time_req < today.replace(hour=10, minute=20):
            package = _package_9_old
        if package.zip_code == zip_code:
            result.append(package)
    return result


# O(n)
def get_packages_by_weight(weight):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.weight == weight:
            result.append(package)
    return result


# O(n)
def get_packages_by_status(status, time_req):
    result = []
    for i in range(1, len(_packages) + 1):
        package = _packages.get(i)
        if package.get_status(time_req).lower() == status.lower():
            result.append(package)
    return result


def set_old_package_9():
    global _package_9_old
    _package_9_old = copy.deepcopy(get_package(9))
    _package_9_old.update_address('300 State St', 'Salt Lake City', 'UT', '84103')


def get_old_package_9():
    return _package_9_old


"""
----------------------
    TRUCK METHODS
----------------------
"""


# O(1)
def put_truck(truck):
    _trucks[truck.id] = truck


# O(1)
def get_truck(truck_id):
    return _trucks[truck_id]


# O(1)
def get_all_trucks():
    return _trucks


# O(1)
def print_metrics(truck_id):
    metrics = get_truck(truck_id).get_metrics()
    print("\n\tTruck", truck_id, "delivery metrics:")
    print("\t\t" + f"{'Departure time: ':<25}" + f"{get_truck(truck_id).get_departure_time().strftime('%I:%M %p'):<20}")
    print("\t\t" + f"{'Packages delivered: ':<25}" + f"{len(metrics['delivered']):<20}")
    # travel = str(metrics['miles']) + ' miles over ' + metrics['time_spent']
    print("\t\t" + f"{'Total miles: ':<25}" + f"{metrics['miles']:<20}")
    print("\t\t" + f"{'Total time spent: ':<25}" + f"{metrics['time_spent']:<20}")
    print("\t\t" + f"{'Return to hub time: ':<25}" + f"{metrics['end_time'].strftime('%I:%M %p'):<20}")


# O(1)
def print_all_metrics():
    print_metrics(1)
    print_metrics(2)
    print_metrics(3)

    total_miles = get_truck(1).get_metrics()['miles'] + get_truck(2).get_metrics()['miles'] + \
                  get_truck(3).get_metrics()['miles']
    total_td = str(get_truck(3).get_metrics()['end_time'] - get_truck(1).get_departure_time()).split(':')
    total_time = f"{int(total_td[0]):01}h {int(total_td[1]):02}m"

    print("\n\t" + f"{'Total miles travelled: ':<29}" + f"{total_miles:<20}")
    print("\t" + f"{'Total delivery time: ':<29}" + f"{total_time:<20}")


"""
-------------------------
    LOCATION METHODS
-------------------------
"""


# O(n)
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
        if location['address'].lower() == address.lower():
            return location


"""
-------------------------
    DISTANCE METHODS
-------------------------
"""


# O(n^2)
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
