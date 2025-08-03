import pygame

WIDTH = 1200
HEIGHT = 600
TITLE = 'Flappy Bird'

screen = pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load('Images/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT + 50))

ground = pygame.image.load('Images/ground.png')
ground = pygame.transform.scale(ground, (1300, 168))

groundX = 0
groundSpeed = 2

clock = pygame.time.Clock()

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        bird1 = pygame.image.load('Images/bird1.png')
        self.images.append(bird1)

        bird2 = pygame.image.load('Images/bird2.png')
        self.images.append(bird2)

        bird3 = pygame.image.load('Images/bird3.png')
        self.images.append(bird3)

        self.index = 0
        self.delay = 0
        self.image = self.images[self.index]

        self.rect = self.images[self.index].get_rect(center = [x, y])

    def update(self):
        self.delay += 1
        if self.delay > 5:
            self.index = 1
            self.delay = 0

            if self.index > 2:
                self.index = 0

        self.image = self.images[self.index]

birdGroup = pygame.sprite.Group()
bird = Bird(50, HEIGHT/2)
birdGroup.add(bird)


def draw():
    global groundX

    while True:
        clock.tick(60)
        
        screen.blit(background, (0, -50))

        birdGroup.draw(screen)
        birdGroup.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        groundX -= 1

        if groundX < -100:
            groundX = 0

        screen.blit(ground, (groundX, 500))

        pygame.display.update()
draw()
