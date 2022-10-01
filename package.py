from hashmap import HashMap
import csv


class Package:

    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def __str__(self):
        return f"{self.id} - {self.address}, {self.city}, {self.state} {self.zip_code} - {self.deadline} - " \
               f"{self.weight} - \"{self.notes}\" - {self.status}"

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def change_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def update_deadline(self, deadline):
        self.deadline = deadline


_packages = HashMap()


def scan_packages():
    with open('data/packages.csv') as file:
        reader = csv.DictReader(file)

        for line in reader:
            package = Package(int(line['id']), line['address'], line['city'], line['state'], line['zip_code'],
                              line['deadline'], int(line['weight']), line['notes'], "at hub")
            _packages.put(package.id, package)


def get_all_packages():
    return _packages


def get_package(package_id):
    return _packages.get(package_id)
