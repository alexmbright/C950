import logistics


class Truck:
    capacity = 16
    speed = 18

    # Time: O(1)
    # Space: O(1)
    def __init__(self, truck_id):
        self.id = truck_id
        self.package_ids = []
        self.departure_time = logistics.today.replace(hour=8, minute=0, second=0)
        self.metrics = None

    # Time: O(1)
    # Space: O(1)
    def load_package(self, package_id):
        self.package_ids.append(package_id)

    # Time: O(1)
    # Space: O(1)
    def load_packages(self, package_ids):
        for pkg in package_ids:
            logistics.get_package(pkg).set_truck(self.id)
            self.package_ids.append(pkg)

    # O(n)
    def unload_package(self, package_id):
        for package_id in self.package_ids:
            if package_id == package_id:
                logistics.get_package(package_id).set_truck(None)
                self.package_ids.remove(package_id)
                return True
        return False

    # O(n)
    def unload_all(self):
        for package_id in self.package_ids:
            logistics.get_package(package_id).set_truck(None)
            self.package_ids.remove(package_id)

    def get_packages(self):
        return self.package_ids

    def set_departure_time(self, time):
        self.departure_time = time

    def get_departure_time(self):
        return self.departure_time

    def set_metrics(self, metrics):
        self.metrics = metrics

    def get_metrics(self):
        return self.metrics
