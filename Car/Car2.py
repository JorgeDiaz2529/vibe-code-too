import random
from PIL import Image
import os
import glob

# Image imports
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load all car sprites
car_sprites = {}
for car_file in glob.glob(os.path.join(current_dir, "Car*.png")):
    sprite_name = os.path.basename(car_file).replace(".png", "").lower()
    car_sprites[sprite_name] = Image.open(car_file)

# Load exclusive sprites for specific cars
madea_sprite = Image.open(os.path.join(current_dir, "Madea.png"))
f1_sprite = Image.open(os.path.join(current_dir, "f1car-removebg-preview.png"))
mystery_machine_sprite = Image.open(os.path.join(current_dir, "Mysterymachine1-1587130271-removebg-preview.png"))

# Sprite mapping: (make, model) -> sprite
sprite_mapping = {
    ("Cadillac", "Sedan de Ville"): madea_sprite,
    ("Ford", "Mustang"): f1_sprite,
    ("Mystery Machine", "Van"): mystery_machine_sprite,
}

# Sprite scale mapping: (make, model) -> (width, height)
# Cars not listed here default to (90, 60)
sprite_scales = {
    ("Ford", "Mustang"): (110, 75),
    ("Toyota", "Camry"): (110, 75),
    ("Honda", "Civic"): (110, 75),
    ("Chevrolet", "Impala"): (110, 75),
    ("Ford", "Bronco"): (110, 75),
    ("Porsche", "911 Carrera GT"): (110, 75),
}

class Car:
    def __init__(self, make, model, license_plate=None, speed=None, sprite=None):
        self.make = make
        self.model = model
        self.license_plate = license_plate or "UNKNOWN"
        self.speed = speed if speed is not None else random.randint(0, 100)
        self.sprite = sprite

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
        super().__init__("Madea Cadillac", "Sedan de Ville", license_plate=license_plate, speed=205, sprite=madea_sprite)


if __name__ == "__main__":
    for c in sample_cars:
        print(f"{c.make} {c.model} ({c.license_plate}) speed: {c.speed} mph")

    special_car = MadeaCatilacSedanDeVille()
    print(f"{special_car.make} {special_car.model} ({special_car.license_plate}) speed: {special_car.speed} mph")