import pygame

#Filepaths
background_path = "Background.jpg"
speedlimit_path = "Speedlimit.png"

#VARIABLES
WIDTH, HEIGHT = 612,408 # background.jpg dimensions
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(background_path)

pygame.display.set_caption("Los pobres Automoviles!") # change later

#GAME LOOP
running = True 
while running:
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #SCREEN FILL
    screen.fill((0,0,0))

    #SPRITES & STUFF
    screen.blit(background, (0,0))

    #DISPLAY
    pygame.display.flip()
    clock.tick(60) #60 fps