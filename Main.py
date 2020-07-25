from Snake2 import *
from training_data import genTrainingData

from keras.models import Sequential
from keras.layers import Dense

# Helper libraries
import numpy as np

# Display Size
display_width = 500
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

# Constants
epochs_no = 5

'''
LEFT -> keyPath = 0
RIGHT -> keyPath = 1
DOWN ->keyPath = 2
UP -> keyPath = 3
'''

training_data_x, training_data_y = genTrainingData(display, fpsClock)

model = Sequential()
model.add(Dense(units=9, input_dim=7),)
model.add(Dense(units=15, activation='relu'),)
model.add(Dense(3, activation='softmax'))


model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit((np.array(training_data_x).reshape(-1, 7)), (np.array(training_data_y).reshape(-1, 3)), batch_size=256,
          epochs=epochs_no)

model.save_weights('snake_model.h5')
model_json = model.to_json()
with open('snake_model.json', 'w') as json_file:
    json_file.write(model_json)
