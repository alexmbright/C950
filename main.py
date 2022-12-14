# Alexander "Alex" Bright - ID: 001130844
import logistics
from truck import Truck
from datetime import datetime

# Greet the user with option to run or cancel the delivery simulation
print("\n\tWelcome to the WGUPS Portal!")
print("\n\tEnter any key to simulate today's deliveries...")
print("\tTo exit the program, type 'exit'\n")

user = input("> ").lower().strip()

# If user chooses to exit, say goodbye and exit the program
if user == 'exit':
    print("\n\tThanks for using the WGUPS Portal! Goodbye...")
    exit()

"""
Call the necessary functions to read and store all data
corresponding to packages, locations, and distances from
their respective CSV files.
"""
logistics.scan_packages()
logistics.scan_locations()
logistics.scan_distances()

# Create and store necessary Truck objects
logistics.put_truck(Truck(1))
logistics.put_truck(Truck(2))
logistics.put_truck(Truck(3))

# Create variable pointing to get_all_trucks() function for ease of use
trucks = logistics.get_all_trucks()

# Manually load packages by hand, making note of all constraints
trucks[1].load_packages([1, 7, 13, 14, 15, 16, 19, 20, 27, 29, 30, 34, 35, 37, 40])
trucks[2].load_packages([3, 6, 18, 25, 26, 28, 31, 32, 36, 38, 39])
trucks[3].load_packages([2, 4, 5, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 33])

# Set appropriate departure times for each truck
trucks[1].set_departure_time(logistics.today.replace(hour=8))
trucks[2].set_departure_time(logistics.today.replace(hour=9, minute=5))
trucks[3].set_departure_time(logistics.today.replace(hour=10, minute=20))

# Run delivery algorithm for each truck
logistics.deliver_packages(trucks[1])
logistics.deliver_packages(trucks[2])
logistics.deliver_packages(trucks[3])

# Create one-time deepcopy of package 9 with old address for use in lookups
logistics.set_old_package_9()

# Print out all truck delivery metrics
logistics.print_all_metrics()

# Create 'flags' dictionary to use in CLI for input validation and back requests
flags = {'exit': False}

# Begin command line interface
while not flags['exit']:

    # Greet the user with available options
    print("\n\tSelect an option:")
    print("\t\t" + f"{'m [1-3]:':<10}\t\tPrint delivery metrics (all, or optional: truck 1-3)")
    print("\t\t" + f"{'a:':<10}\t\tView all package data for the end of the day")
    print("\t\t" + f"{'p:':<10}\t\tLookup packages at specific time")
    print("\t\t" + f"{'exit:':<10}\t\tExit the WGUPS Portal\n")

    user = input("> ").lower().strip()

    # Exit the program if user requests
    if user == 'exit':
        print("\n\tThanks for using the WGUPS Portal! Goodbye...")
        flags['exit'] = True
        continue
    # empty input validation
    if len(user) == 0:
        print("\n\tPlease enter an input...")
        continue
    empty_inputs = 0
    # metric input validation and response
    user_spl = user.split(maxsplit=1)
    if user_spl[0] == 'm':
        if len(user_spl) == 1:
            logistics.print_all_metrics()
            continue
        if len(user_spl) == 2:
            if user_spl[1] != '1' and user_spl[1] != '2' and user_spl[1] != '3':
                print("\n\tEnter a number 1-3! Please try again...")
                continue
            logistics.print_metrics(int(user_spl[1]))
    # input validation
    elif len(user) > 1:
        print("\n\tInvalid input! Please try again...")
        continue
    # view all packages for end of day
    elif user == 'a':
        packages = logistics.get_all_packages()
        if len(packages) == 0:
            print("\n\tNo packages found!\n")
            continue
        print("\n\tPackages found in system:")
        for i in range(1, len(packages) + 1):
            package = logistics.get_package(i)
            print("\t\t" + str(package))
        print("\n\tEnter any key to return...\n")
        input("> ")
        continue
    # package input response (ask for time)
    elif user == 'p':
        flags['valid'] = False
        flags['back'] = False
        time = logistics.today
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
            time_str = time.strftime('%I:%M %p')
            print(f"\n\tTime being used in lookup: {time_str}")
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print("\tPackages found in system:")
                for i in range(1, len(packages) + 1):
                    package = logistics.get_package(i)
                    if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                        package = logistics.get_old_package_9()
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with ID {package.get_id()}:")
                if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                    package = logistics.get_old_package_9()
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with status '{status}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                        package = logistics.get_old_package_9()
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package address lookup
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with address '{user.title()}':")
                for package in packages:
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package city lookup
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with city '{user.title()}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                        package = logistics.get_old_package_9()
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package zip code lookup
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with zip code '{user}':")
                for package in packages:
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package weight lookup
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
                print(f"\n\tTime being used in lookup: {time_str}")
                print(f"\tPackages found with weight '{user}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                        package = logistics.get_old_package_9()
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
            # run package deadline lookup
            elif user == 'd':
                flags['valid'] = False
                flags['back'] = False
                packages = []
                deadlines = {1: logistics.today.replace(hour=9, minute=0),
                             2: logistics.today.replace(hour=10, minute=30),
                             3: logistics.today.replace(hour=17, minute=0)}
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
                print(f"\n\tTime being used in lookup: {time_str}")
                deadline_str = deadline.strftime('%I:%M %p')
                print(f"\tPackages found with deadline '{deadline_str if deadline_str != '05:00 PM' else 'end of day'}':")
                for package in packages:
                    if package.get_id() == 9 and time < logistics.today.replace(hour=10, minute=20):
                        package = logistics.get_old_package_9()
                    print("\t\t" + package.status_str(time))
                print("\n\tEnter any key to return...\n")
                input("> ")
        # if back requested, go back...
        if flags['back']:
            continue
    else:
        print("\n\tInvalid input! Please try again...")

