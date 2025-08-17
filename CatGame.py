import pygame  # Import pygame library
import random  # Import random library

pygame.init()  # Initialize pygame
height = 600  # Set screen height
width = 600  # Set screen width
screen = pygame.display.set_mode((width, height))  # Create game window
pygame.display.set_caption("Cat Catching Game")  # Set window caption

# Load images
cat_img = pygame.image.load("cat.png")  # Load cat image
cat_img = pygame.transform.scale(cat_img, (145,150))  # Scale cat image
fish_img = pygame.image.load("fish.png")  # Load fish image
trash_img = pygame.image.load("trash.png")  # Load trash image
bomb_img = pygame.image.load("bomb.png")  # Load bomb image
background = pygame.image.load("pixil-frame-0.png")  # Load background image
background = pygame.transform.scale(background, (600,600))

font = pygame.font.SysFont(None, 36)  # Set font for text

# Game variables
cat_x = width // 2  # Initial cat x position
cat_y = height - 110  # Initial cat y position
cat_speed = 5  # Cat movement speed

items = []  # List to hold falling items
item_types = ["fish", "trash", "bomb"]  # Types of items
item_imgs = {"fish": fish_img, "trash": trash_img, "bomb": bomb_img}  # Map item types to images
item_speed = 2  # Initial speed of falling items

score = 0  # Initial score
level = 1  # Initial level
lives = 5  # Initial lives
score_to_next_level = 5  # Score needed to reach next level

clock = pygame.time.Clock()  # Create clock object for FPS
running = True  # Game loop control variable

def spawn_item():
    item_type = random.choice(item_types)  # Randomly choose item type
    x = random.randint(0, width - 120)  # Random x position for item
    items.append({"type": item_type, "x": x, "y": 100})  # Add item to items list

def draw():
    screen.blit(background, (0, 0))  # Draw background
    screen.blit(cat_img, (cat_x, cat_y))  # Draw cat
    for item in items:  # Draw each item
        screen.blit(item_imgs[item["type"]], (item["x"], item["y"]))
    score_text = font.render(f"Score: {score}", True, (0,0,0))  # Render score text
    level_text = font.render(f"Level: {level}", True, (0,0,0))  # Render level text
    lives_text = font.render(f"Lives: {lives}", True, (255,0,0))  # Render lives text
    screen.blit(score_text, (10, 10))  # Draw score text
    screen.blit(level_text, (10, 40))  # Draw level text
    screen.blit(lives_text, (10, 70))  # Draw lives text

def reset_items():
    global items  # Use global items list
    items = []  # Clear items list

while running:  # Main game loop
    clock.tick(60)  # Set FPS to 60
    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:  # Quit event
            running = False  # Exit game loop

    keys = pygame.key.get_pressed()  # Get pressed keys
    if keys[pygame.K_LEFT] and cat_x > 0:  # Move cat left
        cat_x -= cat_speed
    if keys[pygame.K_RIGHT] and cat_x < width - 120:  # Move cat right
        cat_x += cat_speed

    # Spawn items
    if random.randint(1, 100) == 1:  # Randomly spawn item
        spawn_item()

    # Move items
    for item in items:  # Move each item down
        item["y"] += item_speed

    # Check collisions
    for item in items[:]:  # Check for collision with cat
        if cat_y < item["y"] + 50 and cat_y + 50 > item["y"]:
            if cat_x < item["x"] + 50 and cat_x + 50 > item["x"]:
                if item["type"] == "fish":  # If item is fish, increase score
                    score += 1
                elif item["type"] == "trash": # If trash or bomb, lose life
                    lives -= 1
                elif item["type"] == "bomb":
                    lives -= 2
                items.remove(item)  # Remove item after collision

    # Remove items off screen
    items = [item for item in items if item["y"] < height]  # Keep items within screen

    # Level up
    if score >= score_to_next_level:  # Check if score reached next level
        level += 1  # Increase level
        score = 0  # Reset score
        item_speed += 2 if level % 5 == 0 else 0  # Increase item speed every 5 levels
        over_text = font.render("Next Level!", True, (0,255,0))  # Render game over text (no background)
        text_rect = over_text.get_rect(center=(width//2, height//2))  # Get text rectangle, center it
        pygame.draw.rect(screen, (0,0,0), text_rect.inflate(40, 20))  # Draw black rectangle behind text, adjust size with inflate
        screen.blit(over_text, text_rect)  # Draw game over text
        pygame.display.flip()  # Update display
        pygame.time.wait(2000)  # Wait 2 seconds
        reset_items()  # Clear items

    draw()  # Draw everything

    # Game over
    if lives <= 0:  # If no lives left
        over_text = font.render("Game Over!", True, (255,0,0))  # Render game over text (no background)
        text_rect = over_text.get_rect(center=(width//2, height//2))  # Get text rectangle, center it
        pygame.draw.rect(screen, (0,0,0), text_rect.inflate(40, 20))  # Draw black rectangle behind text, adjust size with inflate
        screen.blit(over_text, text_rect)  # Draw game over text
        pygame.display.flip()  # Update display
        pygame.time.wait(2000)  # Wait 2 seconds
        running = False  # Exit game loop

    pygame.display.flip()  # Update display

pygame.quit()  # Quit pygame