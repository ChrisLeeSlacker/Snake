"""Snake Game"""

# Main Import
import pygame
import numpy as np
# Additional Imports
from tqdm import tqdm
import random
import math
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 102)
GREEN = (0, 255, 0)


def theSnake(snake_pos, display):
    """"Draw the Snake"""
    for x in snake_pos:
        pygame.draw.rect(display, BLUE, [x[0], x[1], 10, 10])


def theApple(display, apple_pos):
    """Draw the Apple"""
    pygame.draw.rect(display, (0, 255, 0), pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))


def distAppleSnake(apple_pos, snake_pos):
    """Distance from Apple to Snake"""
    return np.linalg.norm(np.array(apple_pos) - np.array(snake_pos[0]))


def startPositions():
    """Define start position"""
    start = [100, 100]
    snake_pos = [[100, 100], [90, 100], [80, 100]]
    apple_pos = [random.randrange(1, 60) * 10, random.randrange(1, 50) * 10]
    score = 3
    return start, snake_pos, apple_pos, score


def createSnake(start, snake_pos, apple_pos, key_path, score):
    """Create the snake"""
    if key_path == 1:
        start[0] += 10
    elif key_path == 0:
        start[0] -= 10
    elif key_path == 2:
        start[1] += 10
    else:
        start[1] -= 10

    if start == apple_pos:
        apple_pos, score = getApple(apple_pos, score)
        snake_pos.insert(0, list(start))

    else:
        snake_pos.insert(0, list(start))
        snake_pos.pop()

    return snake_pos, apple_pos, score


def getApple(apple_pos, score):
    """Get the apple"""
    apple_pos = [random.randrange(1, 60) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_pos, score


def OOB(start):
    """Out of Bounds"""
    if start[0] >= 600 or start[0] < 0 or start[1] >= 500 or start[1] < 0:
        return 1
    else:
        return 0


def suicide(start, snake_pos):
    """Death by own body collision"""
    # start = snake_pos[0]
    if start in snake_pos[1:]:
        return 1
    else:
        return 0


def noPath(snake_pos):
    """Path is blocked"""
    path_vector = np.array(snake_pos[0]) - np.array(snake_pos[1])

    left_path = np.array([path_vector[1], -path_vector[0]])
    right_path = np.array([-path_vector[1], path_vector[0]])

    is_straight_blocked = pathBlocked(snake_pos, path_vector)
    is_left_blocked = pathBlocked(snake_pos, left_path)
    is_right_blocked = pathBlocked(snake_pos, right_path)

    return path_vector, is_straight_blocked, is_left_blocked, is_right_blocked


def pathBlocked(snake_pos, path):
    """Is the path_vector blocked"""
    next_step = snake_pos[0] + path
    start = snake_pos[0]
    if OOB(next_step) == 1 or suicide(next_step.tolist(), snake_pos) == 1:
        return 1
    else:
        return 0


def randomPath(snake_pos, getApple):
    """Generate a random path_vector to apple"""
    path = 0
    if getApple > 0:
        path = 1
    elif getApple < 0:
        path = -1
    else:
        path = 0

    return newPathVector(snake_pos, getApple, path)


def newPathVector(snake_pos, angleApple, path):
    """Vector for the path_vector from snake to apple"""
    path_vector = np.array(snake_pos[0]) - np.array(snake_pos[1])
    left_path = np.array([path_vector[1], -path_vector[0]])
    right_path = np.array([-path_vector[1], path_vector[0]])

    new_path = path_vector

    if path == -1:
        new_path = left_path
    if path == 1:
        new_path = right_path

    key_path = keyPath(new_path)

    return path, key_path


def keyPath(new_path):
    """Key Direction"""
    key_path = 0
    if new_path.tolist() == [10, 0]:
        key_path = 1
    elif new_path.tolist() == [-10, 0]:
        key_path = 0
    elif new_path.tolist() == [0, 10]:
        key_path = 2
    else:
        key_path = 3

    return key_path


def angleApple(snake_pos, apple_pos):
    """Path to Apple"""
    apple_path = np.array(apple_pos) - np.array(snake_pos[0])
    snake_path = np.array(snake_pos[0]) - np.array(snake_pos[1])

    norm_apple_path = np.linalg.norm(apple_path)
    norm_snake_path = np.linalg.norm(snake_path)
    if norm_apple_path == 0:
        norm_apple_path = 10
    if norm_snake_path == 0:
        norm_snake_path = 10

    apple_path_norm = apple_path / norm_apple_path
    snake_path_norm = snake_path / norm_snake_path
    angle = math.atan2(
        apple_path_norm[1] * snake_path_norm[0] - apple_path_norm[0] * snake_path_norm[1],
        apple_path_norm[1] * snake_path_norm[1] + apple_path_norm[0] * snake_path_norm[0]) / math.pi
    return angle, snake_path, apple_path_norm, snake_path_norm


def playGame(start, snake_pos, apple_pos, keyPath, score, display, fpsClock):
    """Play Function"""
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill(BLACK)

        theApple(apple_pos, display)
        theSnake(snake_pos, display)

        snake_pos, apple_pos, score = createSnake(start, snake_pos, apple_pos, keyPath, score)
        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()
        fpsClock.tick(50000)

        return snake_pos, apple_pos, score