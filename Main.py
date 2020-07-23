from Snake2 import *
from training_data import genTrainingData
from tensorflow import keras

# Helper libraries
import numpy as np

# Display Size
display_width = 600
display_height = 500

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initializing the Game
pygame.init()

# Sets Display
display = pygame.display.set_mode((display_width, display_height))
fpsClock = pygame.time.Clock()

'''
LEFT -> keyPath = 0
RIGHT -> keyPath = 1
DOWN ->keyPath = 2
UP -> keyPath = 3
'''

training_data_x, training_data_y = genTrainingData(display, fpsClock)

model = keras.Sequential([
    keras.layers.Dense(units=9, input_dim=7),
    keras.layers.Dense(units=15, activation='relu'),
    keras.layers.Dense(output_dim=3, activation='softmax')
])

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit((np.array(training_data_x).reshape(-1, 7)), (np.array(training_data_y).reshape(-1, 3)), batch_size=256,
          epochs=3)

model.save_weights('snake_model.h5')
model_json = model.to_json()
with open('snake_model.json', 'w') as json_file:
    json_file.write(model_json)
