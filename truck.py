import logistics


class Truck:
    capacity = 16
    speed = 18

    # Time: O(1) - Space: O(1)
    def __init__(self, truck_id):
        self.id = truck_id
        self.package_ids = []
        self.departure_time = logistics.today.replace(hour=8, minute=0, second=0)
        self.metrics = None

    # Time: O(1) - Space: O(1)
    def load_package(self, package_id):
        self.package_ids.append(package_id)

    # Time: O(n^2) - Space: O(1)
    # Take list of package IDs as input and store into truck's package list
    def load_packages(self, package_ids):
        for pkg in package_ids:
            logistics.get_package(pkg).set_truck(self.id)  # O(n)
            self.package_ids.append(pkg)

    # Time: O(n^2) - Space: O(1)
    # Search for and remove package from truck's package list,
    # and also reset package's truck value
    def unload_package(self, package_id):
        for pkg_id in self.package_ids:
            if pkg_id == package_id:
                logistics.get_package(package_id).set_truck(None)  # O(n)
                self.package_ids.remove(package_id)
                return True
        return False

    # Time: O(n^2) - Space: O(1)
    # Remove all packages from truck's package list,
    # and reset their truck values in the process
    def unload_all(self):
        for package_id in self.package_ids:
            logistics.get_package(package_id).set_truck(None)  # O(n)
            self.package_ids.remove(package_id)

    # Time: O(1) - Space: O(1)
    # Return list of package IDs loaded on truck
    def get_packages(self):
        return self.package_ids

    # Time: O(1) - Space: O(1)
    def set_departure_time(self, time):
        self.departure_time = time

    # Time: O(1) - Space: O(1)
    def get_departure_time(self):
        return self.departure_time

    # Time: O(1) - Space: O(1)
    # Take in and update dictionary of delivery metrics
    def set_metrics(self, metrics):
        self.metrics = metrics

    # Time: O(1) - Space: O(1)
    def get_metrics(self):
        return self.metrics
