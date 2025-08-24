import random
import pgzrun

WIDTH = 400
HEIGHT = 600

# Dot properties
dot_x = WIDTH // 2
dot_radius = 10

# Game state
lines = []
score = 0
speed = 2
game_over = False
level = 1

def draw():
    screen.clear()

    # Background color based on level
    if level == 1:
        screen.fill((0, 0, 30))  # Dark blue
    elif level == 2:
        screen.fill((30, 0, 0))  # Dark red

    if game_over:
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=50, color="white")
        screen.draw.text(f"Score: {score}", center=(WIDTH//2, HEIGHT//2 + 40), fontsize=30, color="white")
        screen.draw.text("Press SPACE to restart", center=(WIDTH//2, HEIGHT//2 + 90), fontsize=20, color="gray")
    else:
        # Draw the player dot
        screen.draw.filled_circle((dot_x, HEIGHT - 30), dot_radius, "white")

        # Draw falling lines
        for line in lines:
            screen.draw.line((line[0], line[1]), (line[0], line[1] + 20), "red")

        # Draw score and level
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"Level: {level}", (WIDTH - 120, 10), fontsize=30, color="white")

def update():
    global dot_x, score, speed, game_over, level

    if game_over:
        return

    # Move dot
    if keyboard.left:
        dot_x -= 5
    if keyboard.right:
        dot_x += 5
    dot_x = max(dot_radius, min(WIDTH - dot_radius, dot_x))

    # Move lines
    for line in lines:
        line[1] += speed
        # Collision detection
        if abs(dot_x - line[0]) < dot_radius and HEIGHT - 30 - line[1] < 20:
            game_over = True

    # Remove off-screen lines
    lines[:] = [line for line in lines if line[1] < HEIGHT]

    # Increase score and difficulty
    score += 1

    # Level progression
    if score > 500:
        level = 2
        speed = 4
    elif score > 100:
        speed = 3

    # Line spawn logic based on level
    if level == 1:
        if random.random() < 0.05 + speed * 0.01:
            lines.append([random.randint(20, WIDTH - 20), 0])
    elif level == 2:
        # Chaos mode: bursty lines
        if random.random() < 0.2:
            for _ in range(random.randint(1, 3)):
                lines.append([random.randint(20, WIDTH - 20), 0])

def on_key_down(key):
    global dot_x, lines, score, speed, game_over, level
    if game_over and key == keys.SPACE:
        # Reset game
        dot_x = WIDTH // 2
        lines = []
        score = 0
        speed = 2
        level = 1
        game_over = False


pgzrun.go()