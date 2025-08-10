import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 600
TITLE = 'Flappy Bird'

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load('Images/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT + 50))

ground = pygame.image.load('Images/ground.png')
ground = pygame.transform.scale(ground, (3000, 600))

class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Images/plane.png')
        self.image = pygame.transform.scale(self.image, (200, 80)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

planeGroup = pygame.sprite.Group()
plane = Plane(100, HEIGHT // 2)
planeGroup.add(plane)

groundX = 0

def draw():
    global groundX

    while True:
        screen.blit(background, (0, -50))

        planeGroup.draw(screen)
        planeGroup.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        groundX -= 5
        if groundX < -100:
            groundX = 0

        screen.blit(ground, (groundX, 30))

        pygame.display.update()

draw()