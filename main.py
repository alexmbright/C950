# Alex Bright 001130844

import logistics
from truck import Truck
import datetime

logistics.scan_packages()
logistics.scan_locations()
logistics.scan_distances()

logistics.put_truck(Truck(1))
logistics.put_truck(Truck(2))
logistics.put_truck(Truck(3))

trucks = logistics.get_all_trucks()

trucks[1].load_packages([1, 7, 13, 14, 15, 16, 19, 20, 27, 29, 30, 34, 35, 37, 40])
trucks[2].load_packages([3, 6, 18, 25, 26, 28, 31, 32, 36, 38, 39])
trucks[3].load_packages([2, 4, 5, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 33])

trucks[1].set_departure_time(datetime.datetime(2022, 10, 4, 8, 0))
trucks[2].set_departure_time(datetime.datetime(2022, 10, 4, 9, 5))
trucks[3].set_departure_time(datetime.datetime(2022, 10, 4, 12))

truck1_route = logistics.deliver_packages(trucks[1])

print('Truck 1 delivered', len(truck1_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck1_route['miles'])
print('\tTime spent:', truck1_route['time_spent'])
print('\tReturned to hub at', truck1_route['end_time'].strftime('%I:%M %p'), '\n')

truck2_route = logistics.deliver_packages(trucks[2])

print('Truck 2 delivered', len(truck2_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck2_route['miles'])
print('\tTime spent:', truck2_route['time_spent'])
print('\tReturned to hub at', truck2_route['end_time'].strftime('%I:%M %p'), '\n')

truck3_route = logistics.deliver_packages(trucks[3])

print('Truck 3 delivered', len(truck3_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck3_route['miles'])
print('\tTime spent:', truck3_route['time_spent'])
print('\tReturned to hub at', truck3_route['end_time'].strftime('%I:%M %p'), '\n')

print('Package Metrics at EOD:\n---------------------------')
for i in range(1, 41):
    pkg = logistics.get_package(i)
    print(f"\t{pkg.status_str(logistics.today().replace(hour=23, minute=59, second=59))}")

