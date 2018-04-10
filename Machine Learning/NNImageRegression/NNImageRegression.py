import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from random import randint

from keras.models import Sequential
from keras.layers import Dense, Activation, LeakyReLU
from keras.wrappers.scikit_learn import KerasRegressor
from keras.optimizers import adam
from keras.callbacks import ReduceLROnPlateau
import keras

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

img = mpimg.imread('images/rainbow.jpg')
h, w, depth = img.shape
if depth == 4:
    img = np.delete(img, 3, axis=2)
if np.amax(img) > 1:
    img = img / 255

def randomSample(n=32):
    X = []
    Y = []
    for i in range(n):
        i = randint(0, h-1)
        j = randint(0, w-1)
        X.append([i/h, j/w])
        Y.append(img[i][j])
    return (np.array(X), np.array(Y))

def viewImage(img):
    plt.imshow(img)
    plt.show()

def viewPredictionLowRes(scale=10):
    a = h//scale
    b = w//scale
    entireImage = np.reshape([[[i/a, j/b] for j in range(b)] for i in range(a)], (a*b, 2))
    predictedImage = np.reshape(model.predict(entireImage), (a, b, 3))
    np.clip(predictedImage, 0, 1, out=predictedImage)
    viewImage(predictedImage)

def viewPrediction():
    entireImage = np.reshape([[[i/h, j/w] for j in range(w)] for i in range(h)], (w*h, 2))
    predictedImage = np.reshape(model.predict(entireImage), img.shape)
    np.clip(predictedImage, 0, 1, out=predictedImage)
    viewImage(predictedImage)

def getPredicts(X):
    predictions = model.predict(X)
    if len(colors) > 2:
        return predictions
    return [i for i in predictions]
        
model = Sequential()
shape = (8, 16, 32, 64, 128, 256, 512, 256, 128, 64, 32, 16, 8)
model.add(Dense(shape[0], input_dim=2))
model.add(LeakyReLU())

for layer in shape[1:]:
    model.add(Dense(layer))
    model.add(LeakyReLU())

model.add(Dense(3))
model.compile(optimizer='rmsprop', loss='mse')

history = LossHistory()
#cbs = [ReduceLROnPlateau(monitor='loss', factor=0.9, patience=3, verbose=1), history]
cbs = [history]
steps = 1
while True:
    X, Y = randomSample(5000)
    model.fit(X, Y, epochs=steps, verbose=0, callbacks=cbs)
    print(history.losses[-1])
    viewPredictionLowRes()

