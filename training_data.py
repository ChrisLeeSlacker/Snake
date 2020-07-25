"""Training Data"""
from Snake2 import *


def genTrainingData(display, fpsClock):
    """Generating Training Data"""
    train_data_x = []
    train_data_y = []
    train_games = 1000
    moves_per_game = 2000

    for _ in tqdm(range(train_games)):
        start, snake_pos, apple_pos, score = startPositions()
        old_distApple = distAppleSnake(apple_pos, snake_pos)

        for _ in range(moves_per_game):
            angle, snake_path, apple_path_norm, snake_path_norm = angleApple(
                snake_pos, apple_pos)
            path, keyPath = randomPath(snake_pos, angle)
            path_vector, is_front_blocked, is_left_blocked, is_right_blocked = noPath(snake_pos)

            path, keyPath, train_data_y = gen_train_data_y(snake_pos, angleApple,
                                                           keyPath, path,
                                                           train_data_y, is_front_blocked,
                                                           is_left_blocked, is_right_blocked)

            if is_front_blocked == 1 and is_left_blocked == 1 and is_right_blocked == 1:
                break

            train_data_x.append(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_path_norm[0], snake_path_norm[0],
                 apple_path_norm[1], snake_path_norm[1]])

            snake_pos, apple_pos, score = playGame(start, snake_pos, apple_pos, keyPath, score, display, fpsClock)

    return train_data_x, train_data_y


def gen_train_data_y(snake_pos, angleApple, keyPath, path, train_data_y, is_front_blocked, is_left_blocked,
                     is_right_blocked):
    """Generating Training Data"""
    if path == -1:
        if is_left_blocked == 1:
            if is_front_blocked == 1 and is_right_blocked == 0:
                path, keyPath = newPathVector(snake_pos, 1)
                train_data_y.append([0, 0, 1])
            elif is_front_blocked == 0 and is_right_blocked == 1:
                path, keyPath = newPathVector(snake_pos, 0)
                train_data_y.append([0, 1, 0])
            elif is_front_blocked == 0 and is_right_blocked == 0:
                path, keyPath = newPathVector(snake_pos, 1)
                train_data_y.append([0, 0, 1])
        else:
            train_data_y.append([1, 0, 0])

    elif path == 0:
        if is_front_blocked == 1:
            if is_left_blocked == 1 and is_right_blocked == 0:
                path, keyPath = newPathVector(snake_pos, 1)
                train_data_y.append([0, 0, 1])
            elif is_left_blocked == 0 and is_right_blocked == 1:
                path, keyPath = newPathVector(snake_pos, -1)
                train_data_y.append([1, 0, 0])
            elif is_left_blocked == 0 and is_right_blocked == 0:
                train_data_y.append([0, 0, 1])
                path, keyPath = newPathVector(snake_pos, 1)
        else:
            train_data_y.append([0, 1, 0])
    else:
        if is_right_blocked == 1:
            if is_left_blocked == 1 and is_front_blocked == 0:
                path, keyPath = newPathVector(snake_pos, 0)
                train_data_y.append([0, 1, 0])
            elif is_left_blocked == 0 and is_front_blocked == 1:
                path, keyPath = newPathVector(snake_pos, -1)
                train_data_y.append([1, 0, 0])
            elif is_left_blocked == 0 and is_front_blocked == 0:
                path, keyPath = newPathVector(snake_pos, -1)
                train_data_y.append([1, 0, 0])
        else:
            train_data_y.append([0, 0, 1])

    return path, keyPath, train_data_y
