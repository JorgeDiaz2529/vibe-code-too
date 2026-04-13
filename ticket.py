class Ticket:
    def __init__(self, license_plate, actual_speed):
        self.license_plate = license_plate
        self.actual_speed = actual_speed

    def calculate_fine(actual_speed):
        if actual_speed > 80:
            return 500
        if actual_speed > 70:
            return 300
        if actual_speed > 60:
            return 100
        if actual_speed > 50:
            return 75
        return 0
        
    def issue_ticket(self, license_plate):
        self.license_plate = license_plate