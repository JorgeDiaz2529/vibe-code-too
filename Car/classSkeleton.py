class Radar:
    def __init__(self, speed, liscence_plate, number_of_cars, ticket_quota):
        self.speed = speed
        self.liscence_plate = liscence_plate
        self.number_of_cars = number_of_cars
        self.ticket_quota = ticket_quota

class Ticket:
    def __init__(self, license_plate, actual_speed, fine_amount, car):
        self.license_plate = license_plate
        self.actual_speed = actual_speed
        self.fine_amount = fine_amount
        self.car = car

    def calculate_fine(self, actual_speed, speed_limit):
        if actual_speed > speed_limit:
            return 250
    

    def issue_ticket(self):
        pass