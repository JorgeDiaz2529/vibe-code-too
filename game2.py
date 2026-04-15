import os
import random
import pygame
import pygwidgets
from Car2 import Car, sample_cars
from radarClass2 import LINE1_X, LINE2_X, Radar
from classSkeleton import Ticket

# Filepaths
background_path = "images/Background.jpg"
speedlimit_path = "images/Speedlimit.png"

WIDTH, HEIGHT = 612, 408
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#4/15/2026
ticketButton = pygwidgets.TextButton(screen,(20,300),"Issue Ticket")
issuedTickets = [] # for all tickets issued through the button
unissuedTickets = [] # in case of despawned cars out of range

# Load background or fallback to a solid surface
if os.path.exists(background_path):
    background = pygame.image.load(background_path)
else:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 20))

pygame.display.set_caption("Los pobres Automoviles!")

COLOR_OPTIONS = [
    (220, 50, 50),
    (50, 220, 50),
    (50, 100, 220),
    (220, 220, 50),
    (180, 50, 220),
    (50, 220, 220),
]

ROAD_RECT = pygame.Rect(0, HEIGHT // 2 - 60, WIDTH, 120)
RED_LINE_X = 100
YELLOW_LINE_X = LINE2_X
SPEED_LIMIT = 65

class GameCar:
    def __init__(self, car, color):
        self.car = car
        self.color = color
        self.x = random.randint(-300, -60)
        self.car.x = self.x
        self.passed_red = False
        self.passed_yellow = False
        self.red_shown = False
        self.yellow_shown = False
        self.active = True
        self.last_speed = 0
        self.last_fine = 0
        self.text_color = (255,255,255)

    def update(self):
        if not self.active:
            return
        self.x += 2
        self.car.x = self.x

        if self.x >= RED_LINE_X and not self.passed_red:
            self.passed_red = True
            self.last_speed = self.car.speed

        if self.x >= YELLOW_LINE_X and not self.passed_yellow:
            self.passed_yellow = True
            ticket = Ticket(self.car.license_plate, self.car.speed, 0, self)
            self.last_fine = ticket.calculate_fine(self.car.speed)

            if self.last_fine > 0:
                ticket.fine_amount = self.last_fine
                unissuedTickets.append(ticket)
                # radar.ticket_count += 1

        if self.x > WIDTH + 100:
            self.active = False

    def draw(self, surface):
        car_rect = pygame.Rect(self.x, HEIGHT // 2 - 20, 60, 40)
        pygame.draw.rect(surface, self.color, car_rect)
        label = font.render(self.car.license_plate, True, self.text_color)
        surface.blit(label, (self.x, HEIGHT // 2 - 40))


def calculate_fine(speed_mph):
    if speed_mph > 80:
        return 500
    elif speed_mph > 70:
        return 300
    elif speed_mph > 60:
        return 100
    elif speed_mph > 50:
        return 75
    else:
        return 50


def compute_speed(car):
    if not car.start_time:
        return 0
    end_time = pygame.time.get_ticks() / 1000.0
    time_seconds = end_time - car.start_time
    distance_miles = 100 * 0.0005
    time_hours = time_seconds / 3600.0
    if time_hours <= 0:
        return 0
    return distance_miles / time_hours


def spawn_car():
    template = random.choice(sample_cars)
    license_plate = f"{template.license_plate}-{random.randint(100, 999)}"
    spawned = Car(template.make, template.model, license_plate=license_plate)
    spawned.speed = random.randint(20, 100)
    color = random.choice(COLOR_OPTIONS)
    return GameCar(spawned, color)

#to calculate the total fine of all tickets
def get_total_fine():
    total = 0
    for ticket in issuedTickets:
        total += ticket.fine_amount

    return total


radar = Radar(ticket_quota=10)
cars = [spawn_car() for _ in range(3)]

message_text = ""
money_text = ""

recent_red_car = None
recent_yellow_car = None

running = True
spawn_timer = 0
spawn_interval = 2500
last_spawn_time = pygame.time.get_ticks()

while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #TICKET BUTTON
        if ticketButton.handleEvent(event):
            if len(unissuedTickets) != 0:
                ticket = unissuedTickets.pop()
                issuedTickets.append(ticket)
                radar.ticket_count += 1
                
                ticket.car.text_color = (255,60,60) #indicator
                print(get_total_fine()) #debug

    if now - last_spawn_time >= spawn_interval:
        cars.append(spawn_car())
        last_spawn_time = now
        spawn_interval = random.randint(1500, 3000)

    screen.fill((15, 15, 40))
    screen.blit(background, (0, 0))

    ticketButton.draw()

    pygame.draw.rect(screen, (40, 40, 40), ROAD_RECT)
    pygame.draw.line(screen, (255, 0, 0), (RED_LINE_X, ROAD_RECT.top), (RED_LINE_X, ROAD_RECT.bottom), 4)
    pygame.draw.line(screen, (255, 255, 0), (YELLOW_LINE_X, ROAD_RECT.top), (YELLOW_LINE_X, ROAD_RECT.bottom), 4)
    screen.blit(font.render("MPH line", True, (255, 255, 255)), (RED_LINE_X + 5, ROAD_RECT.top - 24))
    screen.blit(font.render("Fine line", True, (255, 255, 255)), (YELLOW_LINE_X + 5, ROAD_RECT.top - 24))

    for game_car in cars:
        game_car.update()
        game_car.draw(screen)

        if game_car.passed_red and not game_car.red_shown:
            message_text = f"{game_car.car.license_plate} passed {game_car.last_speed:.0f} MPH"
            recent_red_car = game_car
            game_car.red_shown = True

        if game_car.passed_yellow and not game_car.yellow_shown:
            money_text = f"Owes ${game_car.last_fine}" if game_car.last_fine > 0 else "No fine"
            recent_yellow_car = game_car
            game_car.yellow_shown = True
        
        if game_car.x > WIDTH + 100:
            game_car.active = False

    cars = [c for c in cars if c.active]

    hud = font.render(f"Tickets: {radar.ticket_count} / {radar.ticket_quota}", True, (255, 255, 255))
    screen.blit(hud, (20, 20))
    screen.blit(font.render(message_text, True, (255, 255, 255)), (20, 50))
    screen.blit(font.render(money_text, True, (255, 255, 255)), (20, 80))
    screen.blit(font.render(f"Total fine: ${get_total_fine()}", True, (255, 255, 255)), (20, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
