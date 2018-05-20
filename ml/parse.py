import os
import sys
import json
import time
import sklearn
import numpy as np
import pandas as pd
import commands

from numpy import array
from scipy.sparse import csr_matrix
from keras.layers.core import *
from keras.layers.wrappers import TimeDistributed
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.layers.embeddings import Embedding
from keras.utils import np_utils
from keras.metrics import top_k_categorical_accuracy
from keras.models import model_from_json
from keras.callbacks import Callback
from collections import defaultdict
from sklearn import feature_extraction
from sklearn.model_selection import train_test_split


driveData = pd.read_csv('driving_dataset/participant_1.csv', delimiter=";", header=0)

'''
Time_Biotrace		Time_Videorating		Time_Light
Time_Accel			Time_GPS				AccelX
AccelY				AccelZ					Lightning
Latitude_GPS		Longitude_GPS			Accuracy_GPS
Altitude_GPS		Speed_GPS				Bearing_GPS
Frame_Videorating	Rating_Videorating		ECG
SCR					Temp					HR
HRV_LF
'''

# df = pd.DataFrame({'AccelX': driveData['AccelX'],
# 				   'AccelY': driveData['AccelY'],
# 				   'AccelZ': driveData['AccelZ']})
# df.plot.hist(alpha=0.7, bins=100)

# df2 = pd.DataFrame({'GPS Speed': driveData['Speed_GPS']})
# df2	.plot.hist(alpha=0.7, bins=100)
# plt.show()


# maneuverData = pd.read_csv('driving_dataset/maneuver_data/maneuvers.csv', delimiter=',', header=0)
# data = []
# for i in range(len(maneuverData)):
# 	dt = (maneuverData.ix[i]['end_time'] - maneuverData.ix[i]['start_time'])/1000.0
# 	features = [dt, maneuverData.ix[i]['velocity']]
# 	data.append([features, maneuverData.ix[i]['aggressive']])

# print(len(maneuverData))
# print("\n\n")
# print(data)
# print(len(data))


# train_data = np.array([i[0] for i in data[:100]])
# train_target = np.array([i[1] for i in data[:100]])
# test_data = np.array([i[0] for i in data[100:]])
# test_target = np.array([i[1] for i in data[100:]])

maneuverData = pd.read_csv('driving_dataset/maneuver_data/samples_clean_acc.csv', delimiter=',', header=0)
data = []
for i in range(len(maneuverData)):
	x_accel = maneuverData.ix[i]['x_axis']
	y_accel = maneuverData.ix[i]['y_axis']
	z_accel = maneuverData.ix[i]['z_axis']
	features = [x_accel, y_accel, z_accel]
	print("Iteration " + str(i) + "/" + str(len(maneuverData)) + ": [" + str(features) + ", " + str(maneuverData.ix[i]['aggressive']) + "]...")
	data.append([features, maneuverData.ix[i]['aggressive']])

# print(len(maneuverData))
# print("\n\n")
# print(data)
# print(len(data))

dataLen = len(data)
print(dataLen)

train_data = np.array([i[0] for i in data[:dataLen/2]])
train_target = np.array([i[1] for i in data[:dataLen/2]])
test_data = np.array([i[0] for i in data[dataLen/2:]])
test_target = np.array([i[1] for i in data[dataLen/2:]])

model = Sequential()
model.add(Dense(5, activation="relu", kernel_initializer="uniform", input_shape=(3,)))
model.add(Dense(3, init='uniform', activation='softmax'))
model.add(Dense(1, activation="sigmoid", kernel_initializer="uniform"))
model.summary()

model.compile(
	loss='binary_crossentropy',
	optimizer='adam',
	metrics = ['accuracy']
)

results = model.fit(
 train_data, train_target,
 epochs = 50,
 batch_size = 100,
 validation_data = (test_data, test_target)
)

print(np.mean(results.history["val_acc"]))


# # Test
for i in range(40):
	f = [np.random.normal(scale=10), np.random.normal(scale=10), np.random.normal(scale=10)]
	p = model.predict_proba(np.array([f]))
	print("Iteration " + str(i+1) + ": " + str(f) + " ==> " + str(p))
