import logistics


class Package:

    # O(1)
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
        self.late = "Not Late"
        self.truck = None

    # O(1)
    def __str__(self):
        return f"{self.package_id} - {self.address}, {self.city}, {self.state} {self.zip_code} - " \
               f"{self.weight} - \"{self.delivered}\" - {self.delivery_time} - {self.late}"

    # O(1)
    def get_status(self, time):
        truck = logistics.get_truck(self.truck)
        if self.package_id in truck.get_packages() and time < truck.get_departure_time():
            return "at the hub"
        if time < self.delivery_time:
            return "en route"
        return "delivered"

    # O(1)
    def status_str(self, time):
        deadline_str = self.deadline.strftime('%I:%M %p')
        if deadline_str == '11:59 PM':
            deadline_str = 'end of day'
        delivery_time_str = self.delivery_time.strftime('%I:%M %p')
        if self.get_status(time) == "at the hub":
            return f"{self.package_id:02} - AT THE HUB (due by {deadline_str}) - {self.address}, {self.city}, " \
                   f"{self.state} {self.zip_code}"
        if self.get_status(time) == "en route":
            return f"{self.package_id:02} - EN ROUTE on TRUCK {self.truck} (due by {deadline_str}) - {self.address}, {self.city}, " \
                   f"{self.state} {self.zip_code}"
        return f"{self.package_id:02} - DELIVERED at {delivery_time_str} - {self.address}, {self.city}, " \
               f"{self.state} {self.zip_code}"

    # O(1)
    def get_id(self):
        return self.package_id

    # O(1)
    def set_delivered(self, delivered, delivery_time):
        self.delivered = delivered
        self.delivery_time = delivery_time
        if self.delivery_time > self.deadline:
            self.late = "LATE"

    # O(1)
    def get_delivery_time(self):
        return self.delivery_time

    # O(1)
    def update_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    # O(1)
    def set_truck(self, truck):
        self.truck = truck

    # O(1)
    def get_truck(self):
        return self.truck
