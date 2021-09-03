from getdata import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import time

NAME = "Cell-Classifier-{}".format(int(time.time()))
# tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

x = pickle.load(open("x.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))
x = x/255.0

model = Sequential()

model.add(Conv2D(32, (3,3), input_shape=x.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32, (3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32, (3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(256))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("sigmoid"))

# tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

model.compile(loss='binary_crossentropy',  #'binary_crossentropy'
              optimizer= 'adam',
              metrics=['accuracy'])

model.fit(x, y, batch_size=1, epochs = 10,  validation_split=0.05) #change this number , callbacks = [tensorboard]
print("issa good")

