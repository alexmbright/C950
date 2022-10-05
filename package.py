from hashmap import HashMap
import csv
import datetime
import time


class Package:

    def __init__(self, package_id, address, city, state, zip_code, deadline, weight):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.delivered = False
        self.delivery_time = None

    def __str__(self):
        return f"{self.package_id} - {self.address}, {self.city}, {self.state} {self.zip_code} - {self.deadline} - " \
               f"{self.weight} - \"{self.delivered}\" - {self.delivery_time}"

    def get_id(self):
        return self.package_id

    def set_delivered(self, delivered, delivery_time):
        self.delivered = delivered
        self.delivery_time = delivery_time

    def is_delivered(self):
        return self.delivered

    def get_delivery_time(self):
        return self.delivery_time

    def update_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


_packages = HashMap()


def scan_packages():
    with open('data/packages.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            deadline = line['deadline']
            if deadline == 'EOD':
                deadline = "11:59 PM"
            deadline_time = time.strptime(deadline, '%H:%M %p')
            package = Package(int(line['id']), line['address'], line['city'], line['state'], line['zip_code'],
                              deadline_time, int(line['weight']))
            _packages.put(package.package_id, package)


def get_all_packages():
    return _packages


def get_package(package_id):
    return _packages.get(package_id)
