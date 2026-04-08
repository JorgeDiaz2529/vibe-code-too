import time

LINE1_X = 100
LINE2_X = 200
DISTANCE_PIXELS = 100
PIXEL_TO_MILES = 0.01
SPEED_LIMIT = 65  # mph

class Radar:
    def __init__(self, ticket_quota):
        self.ticket_quota = ticket_quota
        
        self.number_of_cars = 0
        self.ticket_count = 0
        
        self.start_program_time = time.time()

    def check_speed(self, car):
        """
        car must have:
        - x (position)
        - license_plate
        - passed_line1
        - start_time
        """

   
        if not car.passed_line1 and car.x >= LINE1_X:
            car.start_time = time.time()
            car.passed_line1 = True

        
        elif car.passed_line1 and car.x >= LINE2_X:
            end_time = time.time()
            time_seconds = end_time - car.start_time

            distance_miles = DISTANCE_PIXELS * PIXEL_TO_MILES
            time_hours = time_seconds / 3600

            speed_mph = distance_miles / time_hours

            self.number_of_cars += 1

            is_speeding = speed_mph > SPEED_LIMIT

            if is_speeding:
                self.ticket_count += 1

            print(f"Car {car.license_plate} speed: {speed_mph:.2f} mph")
            print(f"Speeding: {is_speeding}")

            car.passed_line1 = False

    def cars_per_minute(self):
        elapsed_time = time.time() - self.start_program_time
        minutes = elapsed_time / 60

        if minutes == 0:
            return 0

        return self.number_of_cars / minutes

    def tickets_remaining(self):
        return max(0, self.ticket_quota - self.ticket_count)

    def print_stats(self):
        print("\n--- Radar Stats ---")
        print(f"Total cars: {self.number_of_cars}")
        print(f"Tickets given: {self.ticket_count}")
        print(f"Cars per minute: {self.cars_per_minute():.2f}")
        print(f"Tickets remaining to quota: {self.tickets_remaining()}")