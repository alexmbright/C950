import datetime
import distances
import package

# O(1)
address_updated_9 = False


def deliver_packages(truck, start_time):
    packages = truck.get_packages()
    if not packages:
        return
    # create list of all locations for packages on truck
    package_locations = {}
    locations = []
    for pkg in packages:
        pkg_loc = int(distances.get_location(package.get_package(pkg).address)['id'])
        if pkg_loc not in package_locations:
            package_locations[pkg_loc] = []
        package_locations[pkg_loc].append(pkg)
        locations.append(pkg_loc)
    current_location = 0
    visited_locations = [0]
    current_time = start_time
    total_miles = 0
    delivered = []

    while len(delivered) < len(packages):
        global address_updated_9
        if not address_updated_9 and current_time >= datetime.datetime(2022, 10, 4, 10, 20):
            package.get_package(9).update_address('410 S State St', 'Salt Lake City', 'UT', '84111')
            address_updated_9 = True
        neighbors = distances.get_available(current_location, locations, visited_locations)
        nearest = {}
        for neighbor in neighbors:
            if not nearest:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
                continue
            if neighbor['distance'] < nearest['distance']:
                nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
        for pkg in package_locations.get(nearest['id']):
            nearest_package = package.get_package(pkg)
            delivered.append(nearest_package.get_id())
            nearest_package.set_delivered(True, current_time)
        travel_minutes = (nearest['distance'] / truck.speed) * 60
        current_time += datetime.timedelta(minutes=travel_minutes)
        visited_locations.append(nearest['id'])
        current_location = nearest['id']
        total_miles += nearest['distance']

    # return to hub
    return_miles = distances.get_distance(current_location, 0)
    total_miles += return_miles
    travel_minutes = (return_miles / truck.speed) * 60
    current_time += datetime.timedelta(minutes=travel_minutes)

    hours = int((total_miles // truck.speed))
    minutes = int(((total_miles / truck.speed) * 60) % 60)

    return {'delivered': delivered, 'miles': total_miles, 'end_time': current_time,
            'time_spent': f'{hours}h {minutes}m'}
