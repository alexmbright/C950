# Alex Bright 001130844

import logistics
from truck import Truck

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

trucks[1].set_departure_time(logistics.today().replace(hour=8))
trucks[2].set_departure_time(logistics.today().replace(hour=9, minute=5))
trucks[3].set_departure_time(logistics.today().replace(hour=12))

trucks[1].set_metrics(logistics.deliver_packages(trucks[1]))
trucks[2].set_metrics(logistics.deliver_packages(trucks[2]))
trucks[3].set_metrics(logistics.deliver_packages(trucks[3]))

print("\n\tWelcome to the WGUPS Portal!")
print("\n\tEnter any key to simulate today's deliveries...")
print("\tTo exit the program, type 'exit'\n")

user = input("> ").lower()
if user == 'exit':
    exit()

logistics.print_metrics(1)
logistics.print_metrics(2)
logistics.print_metrics(3)

total_miles = trucks[1].get_metrics()['miles'] + trucks[2].get_metrics()['miles'] + trucks[3].get_metrics()['miles']
total_td = str(trucks[3].get_metrics()['end_time'] - trucks[1].get_departure_time()).split(':')
total_time = f"{int(total_td[0]):01}h {int(total_td[1]):02}m"

print("\n\t" + f"{'Total miles travelled: ':<29}" + f"{total_miles:<20}")
print("\t" + f"{'Total delivery time: ':<29}" + f"{total_time:<20}")

