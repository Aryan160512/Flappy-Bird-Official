import pygame

WIDTH = 1000
HEIGHT = 500
TITLE = 'Self - Designed Infinity Game'

speed = 2

screen = pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load('Images/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT + 50))

ground = pygame.image.load('Images/ground.png')
ground = pygame.transform.scale(ground, (WIDTH + 200, 100))

def draw():
    while True:
        screen.blit(background, (0, -50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        ground.x -= speed
        screen.blit(ground, (0, 400))

        pygame.display.update()
draw()
