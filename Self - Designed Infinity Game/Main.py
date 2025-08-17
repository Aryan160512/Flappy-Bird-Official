import pygame

pygame.init()

WIDTH = 1500
HEIGHT = 800
TITLE = 'Self Designed Game'

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load('Images/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT + 50))

ground = pygame.image.load('Images/ground.png')
ground = pygame.transform.scale(ground, (3000, 800))

flying = False
gameOver = False

class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('Images/plane.png')
        self.original_image = pygame.transform.scale(self.original_image, (200, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0
        self.clicked = False      



    def update(self):
        global flying, gameOver

        if flying:
            self.velocity += 0.5  
            if self.velocity > 5:
                self.velocity = 5
            self.rect.y += int(self.velocity)

        if not gameOver:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.velocity = -10
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            angle = max(min(self.velocity * 2, 25), -10)
            self.image = pygame.transform.rotate(self.original_image, angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, 0)

planeGroup = pygame.sprite.Group()
plane = Plane(100, HEIGHT // 2)
planeGroup.add(plane)

groundX = 0

def draw():
    global groundX, gameOver, flying

    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, -50))

        planeGroup.update()
        planeGroup.draw(screen)

        if plane.rect.bottom >= 575 or plane.rect.top <= 0:
            gameOver = True
            flying = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not gameOver:
                flying = True

        if flying and not gameOver:
            groundX -= 5
            if groundX < -100:
                groundX = 0

        screen.blit(ground, (groundX, 30))
        pygame.display.update()
        clock.tick(60)  

draw()