import os
import pygame
from Car import Car
from radarClass import LINE2_X, Radar
from classSkeleton import Radar as SkeletonRadar, Ticket

# Filepaths
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

pygame.display.set_caption("Los pobres Automoviles!")

# Create a test car and radar objects for runtime validation
car = Car("Toyota", "Camry", license_plate="CAR001")
radar = Radar(ticket_quota=10)

# Example usage of skeleton imports (not used directly in the game loop)
skeleton_radar = SkeletonRadar(speed=0, liscence_plate="SKEL", number_of_cars=0, ticket_quota=5)
sample_ticket = Ticket("CAR001", car.speed, 0)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Advance the test car across the screen and check radar speed once
    car.x += 1
    if car.x == LINE2_X:
        radar.check_speed(car)

    if car.x > WIDTH:
        car.x = 0
        car.passed_line1 = False
        car.start_time = None

    screen.fill((15, 15, 40))
    screen.blit(background, (0, 0))

    # Draw road and radar lines
    road_rect = pygame.Rect(0, HEIGHT // 2 - 60, WIDTH, 120)
    pygame.draw.rect(screen, (40, 40, 40), road_rect)
    pygame.draw.line(screen, (255, 255, 0), (LINE2_X, road_rect.top), (LINE2_X, road_rect.bottom), 4)
    pygame.draw.line(screen, (255, 0, 0), (100, road_rect.top), (100, road_rect.bottom), 4)

    # Draw test car
    car_rect = pygame.Rect(car.x, HEIGHT // 2 - 20, 60, 40)
    pygame.draw.rect(screen, (220, 50, 50), car_rect)

    # Draw HUD text
    speed_text = font.render(f"Car speed: {car.speed} mph", True, (255, 255, 255))
    tickets_text = font.render(f"Tickets issued: {radar.ticket_count}", True, (255, 255, 255))
    screen.blit(speed_text, (20, 20))
    screen.blit(tickets_text, (20, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
