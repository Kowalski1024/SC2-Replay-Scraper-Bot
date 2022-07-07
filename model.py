import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import pickle

datasets = ["data/datasets/" + file for file in os.listdir("data\\datasets")]
state = list(range(0, 75))

train_units = list(range(75, 75+19))
train_structures = list(range(95, 95+15))

clf = RandomForestClassifier(n_estimators=500, max_depth=10)

for idx, file in enumerate(datasets):
    train_X = pd.read_csv(file, skiprows=1, header=None, usecols=state)
    train_y = pd.read_csv(file, skiprows=1, header=None, usecols=train_units+train_structures)
    clf.fit(train_X, train_y)
    print(idx)

filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))
