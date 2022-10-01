import package
import distances

package.scan_packages()

print(package.get_all_packages())

distances.scan_locations()

for location in distances.get_all_locations():
    print(location['id'], "-", location['name'], "\n\t", location['address'], "\n")