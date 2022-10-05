from datetime import datetime, timedelta
import distances

###########
# FIX THIS IMPLEMENTATION OF NEAREST NEIGHBOR
###########

def deliver_packages(truck, start_time):
    packages = truck.get_packages()
    if not packages:
        return
    # create list of all locations for packages on truck
    package_locations = []
    locations = []
    for pkg in packages:
        package_locations.append({'package_id': pkg.package_id, 'location_id': distances.get_location(pkg.address)})
        locations.append(distances.get_location(pkg.address))

    current_time = start_time
    delivered = []

    # deliver first package
    neighbors = distances.get_available(0, package_locations, delivered)
    # find nearest neighbor
    nearest = {}
    for neighbor in neighbors:
        if not nearest:
            nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}
            continue
        if neighbor['distance'] < nearest['distance']:
            nearest = {'id': neighbor['id'], 'distance': neighbor['distance']}

    travel_minutes = (nearest['distance'] / truck.speed) * 60
    current_location = nearest['id']
    current_time += timedelta(minutes=travel_minutes)
    delivered.append(nearest['id'])
