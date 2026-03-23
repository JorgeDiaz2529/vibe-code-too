#Car class
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

        #Randomize car's speed between 0 and 100
        import randome
        self.speed = random.randint(0, 100)

        #Example usage of the cars

        Car1 = Car ("Toyota", "Camry") 
        print("Car1 is a " + Car1.make + " " + Car1.model + " going " + str(Car1.speed) + " mph")
        Car2 = Car ("Honda", "Civic")
        print("Car2 is a " + Car2.make + " " + Car2.model + " going " + str(Car2.speed) + " mph")
        car3 = Car ("Ford", "Mustang")
        print("Car3 is a " + car3.make + " " + car3.model + " going " + str(car3.speed) + " mph")
        car4 = Car ("Chevrolet", "Impala")
        print("Car4 is a " + car4.make + " " + car4.model + " going " + str(car4.speed) + " mph")
        car5 = Car ("Ford", "Bronco")
        print("Car5 is a " + car5.make + " " + car5.model + " going " + str(car5.speed) + " mph")
        car6 = Car ("Porche", "911 carrera GT")
        print("Car6 is a " + car6.make + " " + car6.model + " going " + str(car6.speed) + " mph")
        car7 = Car ("Catialac", "Sedan de ville")
        print("Car7 is a " + car7.make + " " + car7.model + " going " + str(car7.speed) + " mph")
        car8 = Car ("Mystery Machine", "Van")
        print("Car8 is a " + car8.make + " " + car8.model + " going " + str(car8.speed) + " mph")
        
        # Make cars spawn at random intervals between 1 and 5 seconds and print their random speed 
        import time
        import random 
        while True:
            time.sleep(random.randint(1, 5))
            car = Car ("Car", "Model")
            print("A new car has spawned: " + car.make + " " + car.model + " going " + str(car.speed) + " mph")

            #Private class for Madea Catilac Sedan de ville to make it always spawn with a speed of 205 mph
            class MadeaCatilacSedanDeVille(Car):
                def __init__(self):
                    super().__init__("Madea Catilac", "Sedan de ville")
                    self.speed = 205 