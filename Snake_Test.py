"""Testing"""
import tensorflow as tf
from Snake2 import *
from keras.engine.saving import model_from_json
from tensorflow.keras.backend import *

# config = tf.compat.v1.ConfigProto
# tf.compat.v1.GPUOptions(allow_growth=True)          # dynamically grow the memory used on the GPU
# config.log_device_placement = True                  # to log device placement (on which device the operation ran)
# session = tf.compat.v1.Session(config=config)
# tf.compat.v1.keras.backend.set_session(session)     # set this TensorFlow session as the default session for Keras


def playGameWithML(model, display, fpsClock):
    """Start Game with ML"""
    high_score = 3
    avg_score = 0
    test_games = 1000
    moves_per_game = 2500

    for _ in range(test_games):
        start, snake_pos, apple_pos, score = startPositions()

        same_path_count = 0
        prev_path = 0

        for _ in range(moves_per_game):
            path, is_front_blocked, is_left_blocked, is_right_blocked = noPath(
                snake_pos)
            angle, snake_path, apple_path_norm, snake_path_norm = angleApple(
                snake_pos, apple_pos)

            predictions = []
            """Predictions"""
            pre_path = np.argmax(np.array(model.predict(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked,
                 apple_path_norm[0], snake_path_norm[0],
                 apple_path_norm[1], snake_path_norm[1]]).reshape(-1, 7)))) - 1

            if pre_path == prev_path:
                same_path_count += 1
            else:
                same_path_count = 0
                prev_path = pre_path

            new_path = np.array(snake_pos[0]) - np.array(snake_pos[1])
            if pre_path == -1:
                new_path = np.array([new_path[1], -new_path[0]])
            if pre_path == 1:
                new_path = np.array([-new_path[1], new_path[0]])

            key_path = keyPath(new_path)

            next_step = snake_pos[0] + path
            if OOB(snake_pos[0]) == 1 or suicide(next_step.tolist(), snake_pos) == 1:
                break
            snake_pos, apple_pos, score = playGame(start, snake_pos, apple_pos, key_path, score, display, fpsClock)

            if score > high_score:
                high_score = score

        avg_score += score

    return high_score, avg_score / 1000


json_file = open('snake_model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('snake_model.h5')

display_width = 600
display_height = 500

pygame.init()

display = pygame.display.set_mode((display_width, display_height))
fpsClock = pygame.time.Clock()
high_score, avg_score = playGameWithML(model, display, fpsClock)
print("Maximum score achieved is:  ", high_score)
print("Average score achieved is:  ", avg_score)
