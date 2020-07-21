"""Snake Game"""

# Main Import
import pygame
# Additional Imports
import random
import time

# Initialize PyGame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 102)
GREEN = (0, 255, 0)

"""Create the Window below"""
# Display Dimensions
dis_width = 600
dis_height = 400

# Window Size (Tuple)
dis = pygame.display.set_mode((dis_width, dis_height))

# Name of window
pygame.display.set_caption('Snake')

# FPS Clock
fpsClock = pygame.time.Clock()

# Snake Properties
SNAKE_BLK = 10
SNAKE_SPD = 15

# Font
GAME_FONT = pygame.font.SysFont('freesansbold,ttf', 25)
SCORE_FONT = pygame.font.SysFont('freesansbold,ttf', 35)

# Score
score, high_score = (0, 0)


def theScore(score):
    """The Score Function"""
    global high_score
    if score > high_score:
        high_score = score
    value = SCORE_FONT.render(f'Score: {score} High Score: {high_score}', True, GREEN)
    dis.blit(value, [0, 0])


def theSnake(SNAKE_BLK, snake_list):
    """"Drawing our snake and increasing the size"""
    for x in snake_list:
        pygame.draw.rect(dis, BLUE, [x[0], x[1], SNAKE_BLK, SNAKE_BLK])


def message(msg, color):
    """Death Message"""
    mesg = GAME_FONT.render(msg, True, color)
    dis.blit(mesg, [dis_width / 4, dis_height / 3])


def gameLoop():
    """Function for looping the game"""
    # Game state
    game_over = False
    game_close = False

    # Position
    current_pos_x1 = dis_width / 2
    current_pos_y1 = dis_height / 2

    # Variables for updating position
    new_pos_x1 = 0
    new_pos_y1 = 0

    # Snake Size
    snake_list = []
    snake_size = 1

    # Variables for the food placement
    food_x = round(random.randrange(0, dis_width - SNAKE_BLK) / 10.0) * 10.0
    food_y = round(random.randrange(0, dis_height - SNAKE_BLK) / 10.0) * 10.0

    while not game_over:
        """Loop to keep game running"""
        while game_close:
            dis.fill(BLACK)
            message("Game Over! Press [Q]uit or [A]gain", RED)
            theScore(snake_size - 1)
            pygame.display.update()

            """Quit or Retry"""
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_a:
                        gameLoop()

        """Game Events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                """Controls"""
                if event.key == pygame.K_LEFT:
                    new_pos_x1 = -SNAKE_BLK
                    new_pos_y1 = 0
                elif event.key == pygame.K_RIGHT:
                    new_pos_x1 = SNAKE_BLK
                    new_pos_y1 = 0
                elif event.key == pygame.K_UP:
                    new_pos_y1 = -SNAKE_BLK
                    new_pos_x1 = 0
                elif event.key == pygame.K_DOWN:
                    new_pos_y1 = SNAKE_BLK
                    new_pos_x1 = 0

        if current_pos_x1 >= dis_width or current_pos_x1 < 0 or current_pos_y1 >= dis_height or current_pos_y1 < 0:
            """Check if alive"""
            game_close = True

        # Updating the position
        current_pos_x1 += new_pos_x1
        current_pos_y1 += new_pos_y1

        dis.fill(BLACK)

        # Draw the Food
        pygame.draw.rect(dis, RED, [food_x, food_y, SNAKE_BLK, SNAKE_BLK])

        # Snake head
        snake_head = [current_pos_x1, current_pos_y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_size:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        theSnake(SNAKE_BLK, snake_list)
        theScore(snake_size - 1)

        pygame.display.update()

        # Getting Food
        if current_pos_x1 == food_x and current_pos_y1 == food_y:
            food_x = round(random.randrange(0, dis_width - SNAKE_BLK) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_height - SNAKE_BLK) / 10.0) * 10.0
            snake_size += 1

        # Speed of the Snake
        fpsClock.tick(SNAKE_SPD)

    pygame.quit()
    quit()


gameLoop()
