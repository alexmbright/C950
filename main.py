# Alex Bright 001130844

import logistics
import package
import distances
from truck import Truck
import datetime

package.scan_packages()
distances.scan_locations()
distances.scan_distances()

truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

truck1.load_packages([1, 7, 13, 14, 15, 16, 19, 20, 27, 29, 30, 34, 35, 37, 40])
truck2.load_packages([3, 6, 18, 25, 26, 28, 31, 32, 36, 38, 39])
truck3.load_packages([2, 4, 5, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 33])

truck1_start = datetime.datetime(2022, 10, 4, 8, 0)
truck2_start = datetime.datetime(2022, 10, 4, 9, 5)
truck3_start = datetime.datetime(2022, 10, 4, 12)

truck1_route = logistics.deliver_packages(truck1, truck1_start)

print('Truck 1 delivered', len(truck1_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck1_route['miles'])
print('\tTime spent:', truck1_route['time_spent'])
print('\tReturned to hub at', truck1_route['end_time'].strftime('%I:%M %p'), '\n')

truck2_route = logistics.deliver_packages(truck2, truck2_start)

print('Truck 2 delivered', len(truck2_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck2_route['miles'])
print('\tTime spent:', truck2_route['time_spent'])
print('\tReturned to hub at', truck2_route['end_time'].strftime('%I:%M %p'), '\n')

truck3_route = logistics.deliver_packages(truck3, truck3_start)

print('Truck 3 delivered', len(truck3_route['delivered']), 'packages')
print('\tTotal miles traveled:', truck3_route['miles'])
print('\tTime spent:', truck3_route['time_spent'])
print('\tReturned to hub at', truck3_route['end_time'].strftime('%I:%M %p'), '\n')

