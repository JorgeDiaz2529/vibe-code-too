import pygame
import pygwidgets
import radarClass

#Filepaths
background_path = "images/Background.jpg"
speedlimit_path = "images/Speedlimit.png"

#VARIABLES
WIDTH, HEIGHT = 612,408 # background.jpg dimensions
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(background_path)
cars = [] # HOLDS ALL THE CARDS
radar = radarClass.Radar(10)

#WIDGETS
ticketButton = pygwidgets.TextButton(screen,(100,100),"Issue Ticket")

pygame.display.set_caption("Los pobres Automoviles!") # change later

#GAME 
running = True 
while running:
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    if ticketButton.handleEvent(event):
        print("tiget")

    #CARS
    for car in cars:
        #initiate radar functions
        if car.get_rect().collidepoint((0,0)):
            pass

    #SCREEN FILL
    screen.fill((0,0,0))

    #SPRITES & STUFF
    screen.blit(background, (0,0))
    
    #BUTTONS
    ticketButton.draw()

    #DISPLAY
    pygame.display.flip()
    clock.tick(60) #60 fps