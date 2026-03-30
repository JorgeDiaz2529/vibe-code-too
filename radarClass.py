import time

# Constants
LINE1_X = 100
LINE2_X = 200
DISTANCE_PIXELS = 100
PIXEL_TO_MILES = 0.01

class Radar:
    def __init__(self, speed, license_plate, number_of_cars, ticket_quota, x=0, passed_line1=False, start_time=0):
        self.speed = speed
        self.license_plate = license_plate
        self.number_of_cars = number_of_cars
        self.ticket_quota = ticket_quota
        self.x = x
        self.passed_line1 = passed_line1
        self.start_time = start_time
    
    def check_speed(self):
        if not self.passed_line1 and self.x >= LINE1_X:
            self.start_time = time.time()
            self.passed_line1 = True

        elif self.passed_line1 and self.x >= LINE2_X:
            end_time = time.time()
            time_seconds = end_time - self.start_time

            distance_miles = DISTANCE_PIXELS * PIXEL_TO_MILES
            time_hours = time_seconds / 3600

            speed_mph = distance_miles / time_hours

            print(f"Car speed: {speed_mph:.2f} mph")




