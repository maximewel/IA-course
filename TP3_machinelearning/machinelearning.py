"""
Steve Mendes Reis, Maxime Welcklen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

#Initial values for our dataset
labels = ["balanced", "electric_fault", "unbalanced"]
labelsEncoded = {"balanced" : 0, "electric_fault" : 1, "unbalanced" : 2}
speeds = range(75, 105, 5) #75, 80, ..., 100

timeserieTable = []

for label in labels:
    for speed in speeds :
        timeseries = pd.read_csv(f"C:\\DEV\\IA\\TP3_machinelearning\\dataset_SOON_Electric_Engine_Simulator\\2021-03-26\\gray_{speed}_{label}.csv", header=None, names=["a1", "a2", "a3"])

        """
        settings = MinimalFCParameters()
        extract_features(timeseries, default_fc_parameters=settings, column_id="id")

        print(extracted_features)"""

        #Hand-made extraction

        # Unique parameters
        rollingWindow = 500

        #Speed
        timeseries["label"] = labelsEncoded[label]
        #Label encoding
        timeseries["speed"] = speed
        
        maxValues = {"a1" : np.max(np.abs(timeseries["a1"])), "a2" : np.max(np.abs(timeseries["a2"])), "a3" : np.max(np.abs(timeseries["a3"]))}
        # Parameters across accelerations
        for acc in ["a1", "a2", "a3"] :
            #Normalization 
            #timeseries[f"norm_{acc}"] = np.abs(timeseries[acc]) / maxValues[acc]
            timeseries[f"mean_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).mean()
            timeseries[f"std_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).std()
            timeseries[f"min_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).min()
            timeseries[f"max_{acc}"] = timeseries[f"{acc}"].rolling(window=rollingWindow).max()

        #Calculate mean acceleration accross all accelerations
        #timeseries["Mean_accelerations"] = (timeseries["norm_a1"] + timeseries["norm_a2"] + timeseries["norm_a3"]) / 3

        #Delete lines with none values due to rolling window
        first_idx = timeseries['mean_a1'].first_valid_index()
        last_idx = timeseries['mean_a1'].last_valid_index()
        timeseries = timeseries.iloc[first_idx:last_idx]

        #print(timeseries)

        timeserieTable.append(timeseries)

#print("Printing all timeseries")
#print(timeserieTable)

proportionTest = 0.3

timeserieTestTable = []
timeserieTrainTable = []

#Prepare data
for timeserie in timeserieTable :
    #Remove 'working' data not fed to the neural network
    timeserie.drop(columns=['a1', 'a2', 'a3'], inplace=True)
    #split into separate dataframes
    train, test = train_test_split(timeserie, test_size=proportionTest)
    #add to tables
    timeserieTrainTable.append(train)
    timeserieTestTable.append(test)

#Concat features and label, extract label
train = pd.concat(timeserieTrainTable)
y_train = to_categorical(np.asarray(train.pop('label')).astype(np.float32))
x_train = np.asarray(train).astype(np.float32)

test = pd.concat(timeserieTestTable)
y_test = to_categorical(np.asarray(test.pop('label')).astype(np.float32))
x_test = np.asarray(test).astype(np.float32)


#Neural network model building
# My input shape :
# (speed; norma1,2,3; mean norm acc; rolling norm acc1,2,3)
#https://towardsdatascience.com/7-popular-activation-functions-you-should-know-in-deep-learning-and-how-to-use-them-with-keras-and-27b4d838dfe6
#Init layers
#sigmoid - logistic
#tanh - might be interesting because we have negative values with accelerations sometimes
#relu - carefull : neurons can die
#elu - slower than relu
#selu - good and normalizing, only for dense layers
""" Although your mileage will vary, in general SELU > ELU > leaky ReLU (and its variants) > ReLU > tanh > logistic. 
If the network’s architecture prevents it from self-normalizing, then ELU may perform better than SELU (since SELU is not smooth at z = 0). """
model = Sequential()
model.add(layers.Dense(120, activation="relu"))
model.add(layers.Dense(60, activation="elu"))

#model.add(layers.Dense(80, activation="selu"))
#model.add(layers.Dense(50, activation="relu"))
#model.add(layers.Dense(100, activation="tanh")) Doesn't yield great results
#model.add(layers.Dense(100, activation="sigmoid")) Doesn't yield great results

model.add(layers.Dense(len(labels), activation="softmax")) #Get final label, with 3 as we have 3 classes

model.compile(
    loss=keras.losses.CategoricalCrossentropy(),
    optimizer=keras.optimizers.RMSprop(),
    metrics=["accuracy"],
)

history = model.fit(x_train, y_train, batch_size=100, epochs=50, validation_split=0.2)

#Plot from rajinth
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy while training')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

validation_scores = model.evaluate(x_test, y_test, verbose=2)
print(f"Predictions sample : {model.predict(x_test[:10])}")
print(f"Score : loss={validation_scores[0]}, accuracy = {validation_scores[1]}")

#Test to see if printing validation data yields good results :-/
"""
plt.plot(model.predict(x_test), "b", y_test, "r")
plt.title('model accuracy on validation data')
plt.ylabel('accuracy')
plt.xlabel('feature')
plt.legend(['train', 'val'], loc='upper left')
plt.show()"""