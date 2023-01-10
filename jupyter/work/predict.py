import os
from time import time, localtime
import logging
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras import losses, metrics, optimizers
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
import nest_asyncio
from pathlib import Path

nest_asyncio.apply()
SEED = 1337
tf.random.set_seed(SEED)

def most_frequent(List):
    return max(set(List), key=List.count)

test_dir = "/home/jovyan/dataset/GQUIC_small/Test/GQUIC_test_32.feather"
test = pd.read_feather(test_dir)

result = test.groupby('flow_id')['Label'].apply(list).to_dict()
flow_label = []
for flow in result:
    flow_label.append(most_frequent(result[flow]))

flow_label = np.array(flow_label)

true_test = test.drop('flow_id', axis=1)
x_test = true_test.drop('Label', axis=1).to_numpy()/255
x_test = x_test.reshape(-1,20,128,1)

model = tf.keras.models.load_model("/home/jovyan/dataset/model_2")

one_flow = x_test[0].reshape(-1,20,128,1)
print(one_flow)

predictions_1flow = model.predict(one_flow)
one_flow_pred = int(np.argmax(predictions_1flow, axis=-1))
print("Label", one_flow_pred)