import pygame, random

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
birdPassed = False
eaglePassed = False
score = 0

# Enemy spawn timing
ENEMY_FREQUENCY = 5000
EAGLE_FREQUENCY = 10000
lastEnemy = pygame.time.get_ticks() - ENEMY_FREQUENCY
lastEagle = pygame.time.get_ticks() - EAGLE_FREQUENCY

clock = pygame.time.Clock()

class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('Images/plane.png')
        self.original_image = pygame.transform.scale(self.original_image, (200, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.clicked = False

    def update(self):
        global flying, gameOver

        if flying:
            self.velocity += 0.5
            self.velocity = min(self.velocity, 5)
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

class EnemyBird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Images/bird.png')
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        if not gameOver:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.kill()

class EnemyEagle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Images/eagle.png')
        self.image = pygame.transform.scale(self.image, (160, 120))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6

    def update(self):
        if not gameOver:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.kill()

planeGroup = pygame.sprite.Group()
plane = Plane(100, HEIGHT // 2)
planeGroup.add(plane)

enemyGroup = pygame.sprite.Group()
eagleGroup = pygame.sprite.Group()

groundX = 0

def draw():
    global groundX, gameOver, flying, lastEnemy, lastEagle, score, birdPassed, eaglePassed, plane

    while True:
        screen.blit(background, (0, -50))

        pygame.font.init()
        font = pygame.font.SysFont('Calibri', 30)
        text = font.render(f'Score: {int(score)}', True, (0, 0, 0))
        screen.blit(text, (50, 50))

        planeGroup.update()
        enemyGroup.update()
        eagleGroup.update()

        planeGroup.draw(screen)
        enemyGroup.draw(screen)
        eagleGroup.draw(screen)

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

            currentTime = pygame.time.get_ticks()

            if currentTime - lastEnemy > ENEMY_FREQUENCY:
                enemyY = random.randint(100, 600)
                enemy = EnemyBird(WIDTH + 100, enemyY)
                enemyGroup.add(enemy)
                lastEnemy = currentTime

            if currentTime - lastEagle > EAGLE_FREQUENCY:
                eagleY = random.randint(100, 600)
                eagle = EnemyEagle(WIDTH + 200, eagleY)
                eagleGroup.add(eagle)
                lastEagle = currentTime

            if len(enemyGroup):
                bird = enemyGroup.sprites()[0]
                plane = planeGroup.sprites()[0]

                if plane.rect.right > bird.rect.left and plane.rect.left < bird.rect.right and not birdPassed:
                    birdPassed = True
                if birdPassed:
                    score += 0.1
                if plane.rect.left > bird.rect.right:
                    birdPassed = False

            if len(eagleGroup):
                eagle = eagleGroup.sprites()[0]
                plane = planeGroup.sprites()[0]

                if plane.rect.left > eagle.rect.right and not eaglePassed:
                    score += 10
                    eaglePassed = True
                if plane.rect.left < eagle.rect.right:
                    eaglePassed = False

        if (plane.rect.bottom >= 575 or plane.rect.top <= 0 or
            pygame.sprite.groupcollide(planeGroup, enemyGroup, False, False) or
            pygame.sprite.groupcollide(planeGroup, eagleGroup, False, False)):
            gameOver = True
            flying = False

        screen.blit(ground, (groundX, 100))
        pygame.display.update()
        clock.tick(60)

draw()