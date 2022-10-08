import logistics


class Package:

    # Time: O(1) - Space: O(1)
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
        self.truck = None

    # Time: O(1) - Space: O(1)
    def __str__(self):
        return f"{self.package_id} - {self.address}, {self.city}, {self.state} {self.zip_code} - " \
               f"{self.weight} - \"{self.delivered}\" - {self.delivery_time} - {self.late}"

    # Time: O(1) - Space: O(1)
    def get_status(self, time):
        truck = logistics.get_truck(self.truck)
        if self.package_id in truck.get_packages() and time < truck.get_departure_time():
            return "at the hub"
        if time < self.delivery_time:
            return "en route"
        return "delivered"

    # Time: O(1) - Space: O(1)
    def status_str(self, time):
        deadline_str = self.deadline.strftime('%I:%M %p')
        if deadline_str == '05:00 PM':
            deadline_str = 'EOD'
        delivery_time_str = self.delivery_time.strftime('%I:%M %p')
        if self.get_status(time) == "at the hub":
            return f"{self.package_id:02} - \033[01mAT THE HUB\033[0m (due by {deadline_str}) - {self.address}, " \
                   f"{self.city}, {self.state} {self.zip_code}"
        if self.get_status(time) == "en route":
            return f"{self.package_id:02} - \033[01m\033[93mEN ROUTE\033[0m\033[93m on TRUCK {self.truck} " \
                   f"(due by {deadline_str})\033[0m - {self.address}, {self.city}, {self.state} {self.zip_code}"
        return f"{self.package_id:02} - \033[01m\033[32mDELIVERED\033[0m\033[32m at {delivery_time_str}\033[0m - " \
               f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    # Time: O(1) - Space: O(1)
    def get_id(self):
        return self.package_id

    # Time: O(1) - Space: O(1)
    def set_delivered(self, delivered, delivery_time):
        self.delivered = delivered
        self.delivery_time = delivery_time

    # Time: O(1) - Space: O(1)
    def get_delivery_time(self):
        return self.delivery_time

    # Time: O(1) - Space: O(1)
    def update_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    # Time: O(1) - Space: O(1)
    def set_truck(self, truck):
        self.truck = truck

    # Time: O(1) - Space: O(1)
    def get_truck(self):
        return self.truck
