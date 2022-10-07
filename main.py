# Alex Bright 001130844
import copy

import logistics
from truck import Truck
from datetime import datetime

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

user = input("> ").lower().strip()
if user == 'exit':
    exit()

logistics.print_all_metrics()

flags = {'exit': False}
empty_inputs = 0

while not flags['exit']:
    print("\n\tSelect an option:")
    print("\t" + f"{'m [1-3]:':>15}\t\t{'Print delivery metrics (all, or optional: truck 1-3)'}")
    print("\t" + f"{'p:':>15}\t\t{'Lookup packages at specific time'}")
    print("\t" + f"{'exit:':>15}\t\t{'Exit the WGUPS Portal'}\n")

    user = input("> ").lower().strip()
    if user == 'exit':
        print("\n\tThanks for using the WGUPS Portal! Bye...")
        flags['exit'] = True
        continue
    # empty input validation
    if len(user) == 0:
        print("\n\tPlease enter an input...")
        empty_inputs += 1
        if empty_inputs == 2:
            print("\tProgram will exit after 1 more empty entry...")
        elif empty_inputs == 3:
            print("\tToo many empty entries! Exiting program...")
            flags['exit'] = True
        continue
    empty_inputs = 0
    # metric input validation and response
    if user[0] == 'm':
        if len(user) > 3:
            print("\n\tInvalid input! Please try again...")
            continue
        if len(user) == 1:
            logistics.print_all_metrics()
        elif len(user) == 2:
            print("\n\tInvalid input! Please try again...")
            continue
        elif user[2] == '1':
            logistics.print_metrics(1)
        elif user[2] == '2':
            logistics.print_metrics(2)
        elif user[2] == '3':
            logistics.print_metrics(3)
        else:
            print("\n\tInvalid input! Please try again...")
            continue
    # input validation
    elif len(user) > 1:
        print("\n\tInvalid input! Please try again...")
        continue
    # package input response (ask for time)
    elif user == 'p':
        flags['valid'] = False
        flags['back'] = False
        time = logistics.today()
        # time validation and check for back request
        while not flags['valid'] and not flags['back']:
            print("\n\tEnter the time you want to use for looking up packages.")
            print("\t\tFor 12-hour time format, please include a space followed by 'am' or 'pm'.")
            print("\t\tFor 24-hour time format, format as 'HH:MM' (ex: '16:30').")
            print("\t\tTo cancel, type 'back'.\n")
            user = input("> ").lower().strip()
            if len(user) == 0:
                print("\n\tPlease enter an input...")
                continue
            if user == 'back':
                flags['back'] = True
                continue
            user_spl = user.split(":")
            if len(user_spl) != 2:
                print("\n\tInvalid input! Please try again...")
                continue
            if len(user_spl) == 2:
                format_spl = user_spl[1].split()
                # 24-hour format input validation
                if len(format_spl) > 2:
                    print("\n\tInvalid input! Please try again...")
                    continue
                if len(format_spl) == 1:
                    # invalid if not numeric
                    if not user_spl[0].isnumeric() or not user_spl[1].isnumeric():
                        print("\n\tInvalid input! Please try again...")
                        continue
                    # invalid if time out of range
                    if int(user_spl[0]) >= 24 or int(user_spl[0]) < 0 \
                            or int(user_spl[1]) >= 60 or int(user_spl[0]) < 0:
                        print("\n\tTime out of range! Please try again...")
                        continue
                    # set time and flag
                    time_str = f"{int(user_spl[0])}:{int(user_spl[1])}"
                    time = datetime.combine(time, datetime.strptime(time_str, "%H:%M").time())
                    flags['valid'] = True
                    continue
                if len(format_spl) == 2:
                    # invalid if not numeric
                    if not user_spl[0].isnumeric() or not format_spl[0].isnumeric():
                        print("\n\tInvalid input! Please try again...")
                        continue
                    # invalid if not am or pm
                    if format_spl[1] != "am" and format_spl[1] != "pm":
                        print("\n\tInvalid input! Please try again...")
                        continue
                    # invalid if time out of range
                    if int(user_spl[0]) >= 13 or int(user_spl[0]) < 0 \
                            or int(format_spl[0]) >= 60 or int(format_spl[0]) < 0:
                        print("\n\tTime out of range! Please try again...")
                        continue
                    # set time and flag
                    time_str = f"{int(user_spl[0])}:{int(format_spl[0])} {format_spl[1]}"
                    time = datetime.combine(time, datetime.strptime(time_str, "%I:%M %p").time())
                    flags['valid'] = True
        # if back requested, go back...
        if flags['back']:
            continue
        flags['back'] = False
        # run package lookup
        while not flags['back']:
            print(f"\n\tTime being used in lookup: {time.strftime('%I:%M %p')}")
            print("\tSelect a filter:")
            print("\t" + f"{'all:':>10}\t\tView all packages")
            print("\t" + f"{'i:':>10}\t\tPackage ID")
            print("\t" + f"{'s:':>10}\t\tPackage status")
            print("\t" + f"{'a:':>10}\t\tDelivery address")
            print("\t" + f"{'c:':>10}\t\tDelivery city")
            print("\t" + f"{'z:':>10}\t\tDelivery zip code")
            print("\t" + f"{'w:':>10}\t\tDelivery weight")
            print("\t" + f"{'d:':>10}\t\tDelivery deadline")
            print("\t" + f"{'back:':>10}\t\tCancel package lookup\n")
            user = input("> ").lower().strip()
            # invalid if empty input
            if len(user) == 0:
                print("\n\tPlease enter an input...")
                continue
            if user == 'back':
                flags['back'] = True
                continue
            # view all packages
            if user == 'all':
                packages = logistics.get_all_packages()
                if len(packages) == 0:
                    print("\n\tNo packages found!\n")
                    continue
                print("\n\tPackages found in system:")
                for i in range(1, len(packages) + 1):
                    package = logistics.get_package(i)
                    if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                        package = copy.deepcopy(package)
                        package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package ID lookup
            elif user == 'i':
                flags['valid'] = False
                flags['back'] = False
                package = None
                while not flags['valid'] and not flags['back']:
                    print("\n\tEnter package ID to look up.")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    if user == 'back':
                        flags['back'] = True
                        continue
                    # invalid if not numeric
                    if not user.isnumeric():
                        print("\n\tInvalid input! Please try again...")
                        continue
                    package = logistics.get_package(int(user))
                    # validate package found
                    if package is None:
                        print("\n\tNo packages found with that ID! Please try again...")
                        continue
                    # set flag
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with ID {package.get_id()}:")
                if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                    package = copy.deepcopy(package)
                    package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package status lookup
            elif user == 's':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                statuses = {1: 'at the hub', 2: 'en route', 3: 'delivered'}
                while not flags['valid'] and not flags['back']:
                    print("\n\tSelect a status:")
                    print("\t" + f"{'1:':>10}\t\t\033[01mAT THE HUB\033[0m")
                    print("\t" + f"{'2:':>10}\t\t\033[01m\033[93mEN ROUTE\033[0m")
                    print("\t" + f"{'3:':>10}\t\t\033[01m\033[32mDELIVERED\033[0m")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    if user != '1' and user != '2' and user != '3':
                        print("\n\tInvalid input! Please try again...")
                        continue
                    status = statuses[int(user)]
                    packages = logistics.get_packages_by_status(status, time)
                    if len(packages) == 0:
                        print("\n\tNo packages found with that status! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with status '{status}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                        package = copy.deepcopy(package)
                        package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            elif user == 'a':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                while not flags['valid'] and not flags['back']:
                    print("\n\tEnter the address to look up (case-insensitive).")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    packages = logistics.get_packages_by_address(user, time)
                    if len(packages) == 0:
                        print("\n\tNo packages found with that address! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with address '{user.title()}':")
                for package in packages:
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            elif user == 'c':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                while not flags['valid'] and not flags['back']:
                    print("\n\tEnter the city to look up (case-insensitive).")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    packages = logistics.get_packages_by_city(user)
                    if len(packages) == 0:
                        print("\n\tNo packages found with that city! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with city '{user.title()}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                        package = copy.deepcopy(package)
                        package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            elif user == 'z':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                while not flags['valid'] and not flags['back']:
                    print("\n\tEnter the zip code to look up.")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    if not user.isnumeric():
                        print("\n\tInvalid input! Please try again...")
                        continue
                    packages = logistics.get_packages_by_zip(user, time)
                    if len(packages) == 0:
                        print("\n\tNo packages found with that zip code! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with zip code '{user}':")
                for package in packages:
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            elif user == 'w':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                while not flags['valid'] and not flags['back']:
                    print("\n\tEnter the package weight to look up (kg).")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    if not user.isnumeric():
                        print("\n\tInvalid input! Please try again...")
                        continue
                    packages = logistics.get_packages_by_weight(int(user))
                    if len(packages) == 0:
                        print("\n\tNo packages found with that weight! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with weight '{user}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                        package = copy.deepcopy(package)
                        package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            elif user == 'd':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                deadlines = {1: logistics.today().replace(hour=9, minute=0),
                             2: logistics.today().replace(hour=10, minute=30),
                             3: logistics.today().replace(hour=23, minute=59)}
                while not flags['valid'] and not flags['back']:
                    print("\n\tSelect a deadline:")
                    print(f"\t{'1:':>10}\t\t9:00 AM")
                    print(f"\t{'2:':>10}\t\t10:30 AM")
                    print(f"\t{'3:':>10}\t\tEnd of day")
                    print("\tTo cancel, type 'back'\n")
                    user = input("> ").lower().strip()
                    if user == 'back':
                        flags['back'] = True
                        continue
                    if len(user) == 0:
                        print("\n\tPlease enter an input...")
                        continue
                    if user != '1' and user != '2' and user != '3':
                        print("\n\tInvalid input! Please try again...")
                        continue
                    deadline = deadlines[int(user)]
                    packages = logistics.get_packages_by_deadline(deadline)
                    if len(packages) == 0:
                        print("\n\tNo packages found with that deadline! Please try again...")
                        continue
                    flags['valid'] = True
                if flags['back']:
                    flags['back'] = False
                    continue
                print(f"\n\tPackages found with deadline '{deadline.strftime('%I:%M %p')}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today().replace(hour=10, minute=20):
                        package = copy.deepcopy(package)
                        package.update_address('300 State St', 'Salt Lake City', 'UT', '84103')
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
        # if back requested, go back...
        if flags['back']:
            continue
    else:
        print("\n\tInvalid input! Please try again...")
        continue