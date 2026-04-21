import os
import random
import sys
import pygame
from PIL import Image
sys.path.append('..')
from Car2 import Car, sample_cars, car_sprites, sprite_mapping, sprite_scales
from radarClass2 import LINE1_X, LINE2_X, Radar
from classSkeleton import Ticket
from slider import Slider

# Filepaths
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = "Background.jpg"
speedlimit_path = "Speedlimit.png"

WIDTH, HEIGHT = 612, 408
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background or fallback to a solid surface
if os.path.exists(background_path):
    background = pygame.image.load(background_path)
else:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 20))

pygame.display.set_caption("GSP Radar Game!")

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

speed_limit = 65
slider = Slider(10, HEIGHT - 50, 200, 30, 100, 65)

class GameCar:
    def __init__(self, car, color):
        self.car = car
        self.color = color
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

    def update(self):
        if not self.active:
            return
        
        # Proximity-based speed modulation with lane separation
        ahead_cars = [c for c in cars if c.x > self.x and c.lane == self.lane and c != self]
        move_increment = self.car.speed / 10
        if ahead_cars:
            closest_ahead = min(ahead_cars, key=lambda c: c.x - self.x)
            distance = closest_ahead.x - self.x
            min_distance = 100  # pixels (updated for 90px car width)
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
            if self.car.speed > speed_limit:
                ticket = Ticket(self.car.license_plate, self.car.speed, 0)
                self.last_fine = ticket.calculate_fine(self.car.speed, speed_limit)
                if self.last_fine > 0:
                    radar.ticket_count += 1
                    global last_fine
                    last_fine = self.last_fine
            else:
                self.last_fine = 0

        if self.x > WIDTH + 100:
            self.active = False

    def draw(self, surface):
        # Draw sprite if available, otherwise draw colored rectangle
        if self.car.sprite:
            # Convert PIL Image to pygame surface more reliably
            pil_image = self.car.sprite
            
            # Handle different image modes
            if pil_image.mode == 'RGBA':
                pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, 'RGBA')
            elif pil_image.mode == 'RGB':
                pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, 'RGB')
            else:
                # Convert to RGB if other mode
                pil_image = pil_image.convert('RGB')
                pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, 'RGB')
            
            # Scale sprite to fit car area - increased size for better visibility
            scaled_sprite = pygame.transform.scale(pygame_image, (90, 60))
            surface.blit(scaled_sprite, (self.x, lane_ys[self.lane] - 30))
        else:
            # Fallback to colored rectangle if no sprite
            car_rect = pygame.Rect(self.x, lane_ys[self.lane] - 30, 90, 60)
            pygame.draw.rect(surface, self.color, car_rect)
        
        label = font.render(f"{self.car.license_plate}: {self.car.speed} MPH", True, (255, 255, 255))
        surface.blit(label, (self.x, lane_ys[self.lane] - 50))


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
    
    # Check if this car type has a specific sprite mapping
    car_key = (spawned.make, spawned.model)
    if car_key in sprite_mapping:
        spawned.sprite = sprite_mapping[car_key]
    # Otherwise assign a random sprite from available car sprites
    elif car_sprites:
        spawned.sprite = list(car_sprites.values())[random.randint(0, len(car_sprites) - 1)]
    
    color = random.choice(COLOR_OPTIONS)
    game_car = GameCar(spawned, color)
    
    # Spawn before the two-line marker (red at 100, yellow at 200)
    spawn_x = -120
    if cars:
        # Find the rightmost car in the same lane (updated for 90px car width)
        same_lane_cars = [c for c in cars if c.lane == game_car.lane]
        if same_lane_cars:
            rightmost_x = max(c.x + 90 for c in same_lane_cars)
            spawn_x = min(spawn_x, rightmost_x - 140)
    
    game_car.x = spawn_x
    game_car.car.x = game_car.x
    return game_car

radar = Radar(ticket_quota=10)
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
        slider.handle_event(event)

    speed_limit = int(slider.value)

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

    slider.draw(screen, font)

    # Display ticket count
    text_parts = [f"Tickets: {radar.ticket_count}", f"Speed Limit: {speed_limit} MPH"]
    if last_red_speed is not None:
        text_parts.append(f"Last Speed: {last_red_speed} MPH")
    if last_fine is not None:
        text_parts.append(f"Fine: ${last_fine}")
    ticket_text = font.render(" ".join(text_parts), True, (255, 255, 255))
    screen.blit(ticket_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
