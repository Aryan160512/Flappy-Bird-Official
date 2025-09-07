import pygame, random

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
scrollSpeed = 4


flying = False
gameOver = False

PIPE_GAP = 150
PIPE_FREQUENCY = 2000
lastPipe = pygame.time.get_ticks() - PIPE_FREQUENCY
pipePassed = False

score = 0

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
        self.velocity = 0
        self.clicked = False
        self.rect = self.images[self.index].get_rect(center = [x, y])

    def update(self):
        if flying == True:
            self.velocity += 0.5

            if self.velocity > 5:
                self.velocity = 5
            
            if self.rect.bottom < 500:
                self.rect.y += int(self.velocity)

        if gameOver == False:
            if flying == True:
                self.delay += 1

                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.velocity = -10
                    self.clicked = True
                
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                if self.delay > 10:
                    self.index += 1
                    self.delay = 0

                    if self.index > 2:
                        self.index = 0

                self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -180)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Images/pipe.png')
        self.rect = self.image.get_rect()
        
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP/2)]
        elif pos == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP/2)]

    def update(self):
        self.rect.x -= scrollSpeed

        if self.rect.right < 0:
            self.kill()


birdGroup = pygame.sprite.Group()
bird = Bird(50, HEIGHT/2)
birdGroup.add(bird)

pipeGroup = pygame.sprite.Group()

pygame.font.init()
font = pygame.font.SysFont('Calibri', 30)

def gameEnd():
    global gameOver, flying

    gameOver = True
    flying = False
    screen.fill('white')
    message1 = font.render('GAME OVER', True, (255, 0, 0))
    message2 = font.render('Press SPACEBAR to restart the game', True, (255, 0, 0))
    screen.blit(message1, (int(WIDTH / 2 - 80), int(HEIGHT / 2 - 100)))
    screen.blit(message2, (int(WIDTH/2 - 200), int(HEIGHT / 2)))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset()
        
def reset():
    global gameOver, flying, score

    gameOver = False
    flying = False
    score = 0

def draw():
    global groundX, flying, gameOver, lastPipe, pipePassed, score, PIPE_FREQUENCY

    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
                flying = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if gameOver == True:
                        reset()
        
        if gameOver == False:

            screen.blit(background, (0, -50))
            screen.blit(ground, (groundX, 500))

        scoreText = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(scoreText, (50, 50))

        birdGroup.draw(screen)
        pipeGroup.draw(screen)

        birdGroup.update()
        
        if len(pipeGroup) > 0:
            if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.left \
            and birdGroup.sprites()[0].rect.right < pipeGroup.sprites()[0].rect.right \
            and pipePassed == False:
                
                pipePassed = True
            
            if pipePassed == True:
                if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.right:
                    score += 10
                    pipePassed = False

        if bird.rect.bottom >= 500 or bird.rect.top < 0:
            gameEnd()

        if gameOver == False and flying == True:
            groundX -= scrollSpeed

            if groundX < -100:
                groundX = 0

            currentTime = pygame.time.get_ticks()

            if currentTime - lastPipe > PIPE_FREQUENCY:
                pipeHeight = random.randint(-100, 100)
                bottomPipe = Pipe(WIDTH, int(HEIGHT/2) + pipeHeight, -1)
                topPipe = Pipe(WIDTH, int(HEIGHT/2) + pipeHeight, 1)

                pipeGroup.add(bottomPipe)
                pipeGroup.add(topPipe)
                lastPipe = currentTime

                #lastPipe = pygame.time.get_ticks()
                
            pipeGroup.update()

        if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False):
            gameEnd()

        pygame.display.update()
draw()
