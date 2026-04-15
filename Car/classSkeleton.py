class Radar:
    def __init__(self, speed, liscence_plate, number_of_cars, ticket_quota):
        self.speed = speed
        self.liscence_plate = liscence_plate
        self.number_of_cars = number_of_cars
        self.ticket_quota = ticket_quota

class Ticket:
    def __init__(self, license_plate, actual_speed, fine_amount):
        self.license_plate = license_plate
        self.actual_speed = actual_speed
        self.fine_amount = fine_amount

    def calculate_fine(self, actual_speed):
        if actual_speed > 80:
            return 500
        elif actual_speed > 70:
            return 300
        elif actual_speed > 60:
            return 100
        elif actual_speed > 50:
            return 75
        elif actual_speed < 30:
            return 150
        else:
            return 0
    

    def issue_ticket(self):
        pass