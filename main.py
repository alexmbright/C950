import package
import distances
from truck import Truck
import datetime

package.scan_packages()

print(package.get_all_packages())

distances.scan_locations()
distances.scan_distances()

for location in distances.get_all_locations():
    print(location['id'], "-", location['name'], "\n\t", location['address'], "\n")

print("Distances from 2:", distances.get_all_available(2, None))

visited = [6, 10]

print("Distances from 2 with visited 6 and 10:", distances.get_all_available(2, visited))

print("Distance from 1 to 8:", distances.get_distance(1, 8))

test_locations = [5, 7, 9, 15, 17, 19, 24, 26]

print("Distance from 16 to [5, 7, 9, 15, 17, 19, 24, 26]\n", distances.get_available(16, test_locations, None))
print("Distance from 16 to 5:", distances.get_distance(16, 5))

print ("Distance from 8 to 1:", distances.get_distance(8, 1))

print ("Distance from 8 to 8:", distances.get_distance(8, 8))

