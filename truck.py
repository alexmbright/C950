import package
import datetime
import logistics


class Truck:
    capacity = 16
    speed = 18

    def __init__(self, id):
        self.id = id
        self.package_ids = []
        self.departure_time = logistics.today().replace(hour=8, minute=0, second=0)

    def load_package(self, id):
        self.package_ids.append(id)

    def load_packages(self, package_ids):
        for pkg in package_ids:
            self.package_ids.append(pkg)

    def unload_package(self, id):
        for package_id in self.package_ids:
            if package_id == id:
                self.package_ids.remove(id)
                return True
        return False

    def unload_all(self):
        self.package_ids = []

    def get_packages(self):
        return self.package_ids

    def set_departure_time(self, time):
        self.departure_time = time

    def get_departure_time(self):
        return self.departure_time
