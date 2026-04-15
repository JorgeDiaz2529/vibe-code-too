import random

class Car:
    def __init__(self, make, model, license_plate=None, speed=None):
        self.make = make
        self.model = model
        self.license_plate = license_plate or "UNKNOWN"
        self.speed = speed if speed is not None else random.randint(0, 100)

        self.x = 0
        self.passed_line1 = False
        self.start_time = None

    def __repr__(self):
        return f"<Car {self.make} {self.model} {self.license_plate} {self.speed} mph>"


# Sample car definitions for testing and game use
sample_cars = [
    Car("Toyota", "Camry", "Toyota Camry"),
    Car("Honda", "Civic", "Honda Civic"),
    Car("Ford", "Mustang", "Ford Mustang"),
    Car("Chevrolet", "Impala", "Chevrolet Impala"),
    Car("Ford", "Bronco", "Ford Bronco"),
    Car("Porsche", "911 Carrera GT", "Porsche 911 Carrera GT"),
    Car("Cadillac", "Sedan de Ville", "Cadillac Sedan de Ville"),
    Car("Mystery Machine", "Van", "Mystery Machine Van"),
]


class MadeaCatilacSedanDeVille(Car):
    def __init__(self, license_plate="CAR009"):
        super().__init__("Madea Cadillac", "Sedan de Ville", license_plate=license_plate, speed=205)


if __name__ == "__main__":
    for c in sample_cars:
        print(f"{c.make} {c.model} ({c.license_plate}) speed: {c.speed} mph")

    special_car = MadeaCatilacSedanDeVille()
    print(f"{special_car.make} {special_car.model} ({special_car.license_plate}) speed: {special_car.speed} mph")