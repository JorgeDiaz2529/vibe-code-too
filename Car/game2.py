import os
import random
import pygame
from Car2 import Car, sample_cars
from radarClass2 import LINE1_X, LINE2_X, Radar
from classSkeleton import Ticket
import pygwidgets

# Filepaths
background_path = ".\images\Background.jpg"
speedlimit_path = ".\images\Speedlimit.png"

WIDTH, HEIGHT = 612, 408
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#TICKETS
ticket_button = pygwidgets.TextButton(screen, (0,310), "Issue Ticket")
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
LANE_COUNT = 3
lane_ys = [HEIGHT // 2 - 40, HEIGHT // 2, HEIGHT // 2 + 40]

class GameCar:
    def __init__(self, car, color):
        self.car = car
        self.color = color
        self.text_color = (255,255,255)
        self.x = random.randint(-300, -60)
        self.car.x = self.x
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.passed_red = False
        self.passed_yellow = False
        self.red_shown = False
        self.yellow_shown = False
        self.active = True
        self.last_speed = 0
        self.last_fine = 0
        self.ticket = None

    def update(self):
        if not self.active:
            return
        
        # Proximity-based speed modulation with lane separation
        ahead_cars = [c for c in cars if c.x > self.x and c.lane == self.lane and c != self]
        move_increment = self.car.speed / 10
        if ahead_cars:
            closest_ahead = min(ahead_cars, key=lambda c: c.x - self.x)
            distance = closest_ahead.x - self.x
            min_distance = 70  # pixels
            if distance <= min_distance:
                move_increment = 0  # Stop to avoid collision
            else:
                move_increment = min(move_increment, distance - min_distance)
        
        self.x += move_increment
        self.car.x = self.x

        if self.x >= RED_LINE_X and not self.passed_red:
            self.passed_red = True
            self.last_speed = self.car.speed
            global last_red_speed
            last_red_speed = self.car.speed

        if self.x >= YELLOW_LINE_X and not self.passed_yellow:
            self.passed_yellow = True
            self.ticket = Ticket(self.car.license_plate, self.car.speed, 0, self)
            self.last_fine = self.ticket.calculate_fine(self.car.speed)

            if self.last_fine > 0:
                self.ticket.fine_amount = self.last_fine
                unissuedTickets.append(self.ticket)

                global last_fine
                last_fine = self.last_fine

        if self.x > WIDTH + 100:
            if self.ticket is not None and self.ticket in unissuedTickets:
                unissuedTickets.remove(self.ticket)

            self.active = False

    def draw(self, surface):
        car_rect = pygame.Rect(self.x, lane_ys[self.lane] - 20, 60, 40)
        pygame.draw.rect(surface, self.color, car_rect)
        label = font.render(f"{self.car.license_plate}: {self.car.speed} MPH", True, self.text_color)
        surface.blit(label, (self.x, lane_ys[self.lane] - 40))


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
    game_car = GameCar(spawned, color)
    
    # Spawn before the two-line marker (red at 100, yellow at 200)
    spawn_x = -120
    if cars:
        # Find the rightmost car in the same lane
        same_lane_cars = [c for c in cars if c.lane == game_car.lane]
        if same_lane_cars:
            rightmost_x = max(c.x + 60 for c in same_lane_cars)
            spawn_x = min(spawn_x, rightmost_x - 140)
    
    game_car.x = spawn_x
    game_car.car.x = game_car.x
    return game_car

def get_total_fine():
    total = 0
    for ticket in issuedTickets:
        total += ticket.fine_amount

    return total

radar = Radar(ticket_quota=5)
cars = []
for i in range(3):
    car = spawn_car()
    car.x = -120 - i * 80  # Space initial cars before the lines
    car.car.x = car.x
    cars.append(car)

message_text = ""
money_text = ""

recent_red_car = None
recent_yellow_car = None
last_red_speed = None
last_fine = None

running = True
spawn_timer = 0
spawn_interval = 2000
last_spawn_time = pygame.time.get_ticks()

while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if ticket_button.handleEvent(event):
            if len(unissuedTickets) != 0 and radar.ticket_count < radar.ticket_quota:
                ticket = unissuedTickets.pop()
                issuedTickets.append(ticket)
                radar.ticket_count += 1
                
                ticket.car.text_color = (255,30,30) #indicator
                print(get_total_fine()) #debug
            elif len(unissuedTickets) == 0:
                print("no tickets!")

    if now - last_spawn_time >= spawn_interval:
        cars.append(spawn_car())
        last_spawn_time = now
        spawn_interval = random.randint(1500, 3000)

    screen.fill((15, 15, 40))
    screen.blit(background, (0, 0))

    # Draw road
    pygame.draw.rect(screen, (50, 50, 50), ROAD_RECT)

    # Draw lines
    pygame.draw.line(screen, (255, 0, 0), (RED_LINE_X, 0), (RED_LINE_X, HEIGHT), 2)
    pygame.draw.line(screen, (255, 255, 0), (YELLOW_LINE_X, 0), (YELLOW_LINE_X, HEIGHT), 2)

    # Update and draw cars
    for car in cars[:]:
        car.update()
        if not car.active:
            cars.remove(car)
        else:
            car.draw(screen)

    # Display ticket count
    text_parts = [f"Tickets: {radar.ticket_count}/{radar.ticket_quota}"]
    if last_red_speed is not None:
        text_parts.append(f"Last Speed: {last_red_speed} MPH")
    if last_fine is not None:
        text_parts.append(f"Fine: ${last_fine}")
    ticket_text = font.render(" ".join(text_parts), True, (255, 255, 255))
    screen.blit(ticket_text, (10, 10))

    ticket_button.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
