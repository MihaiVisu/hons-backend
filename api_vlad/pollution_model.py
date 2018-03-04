import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

# Boiling
filename = '009Boiling-2018-02-15-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data1 = pd.read_csv(data, delimiter = ',')
filename = '010Boiling-2018-02-16-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data2 = pd.read_csv(data, delimiter = ',')
filename = '023Boiling-2018-03-01.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data3 = pd.read_csv(data, delimiter = ',')
boiling = pd.concat([data1, data2, data3], ignore_index=True)
boiling = boiling.fillna(value=0)

# Candle Burning
filename1 = '001Indoor-Hoover-Candle-2018-02-06-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
data = pd.read_csv(data, delimiter = ',')
candle = data[data['label'] == 5]
candle = candle.reset_index()
candle = candle.fillna(value=0)

# Frying
filename1 = '006Frying-2018-02-07.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
frying_data1 = pd.read_csv(data, delimiter = ',')
filename1 = '007Frying-2018-02-01.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
frying_data2 = pd.read_csv(data, delimiter = ',')
filename1 = '005Frying-Outdoor-2018-02-13-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
frying_data3 = pd.read_csv(data, delimiter = ',')
frying_data3 = frying_data3[frying_data3['label'] == 2]
frying = pd.concat([frying_data1, frying_data2, frying_data3], ignore_index=True)
frying = frying.fillna(value=0)


# Hoovering
filename1 = '001Indoor-Hoover-Candle-2018-02-06-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
data1 = pd.read_csv(data, delimiter = ',')
filename1 = '020Hoover-2018-02-27.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
data2 = pd.read_csv(data, delimiter = ',')
data1 = data1[data1['label'] == 4]
hoovering = pd.concat([data1, data2],ignore_index=True)
hoovering = hoovering.fillna(value=0)

# Smoking
filename1 = '008Smoking_Inside-2018-02-07.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename1)
smoking_inside_data = pd.read_csv(data, delimiter = ',')
smoking_inside_data = smoking_inside_data[smoking_inside_data['bin0'] > 2500]
filename3 = '017Smoking_Inside-2018-02-28.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename3)
smoking_inside_data1 = pd.read_csv(data, delimiter = ',')
smoking_inside_data1 = smoking_inside_data1[smoking_inside_data1['bin0'] > 2500]
smoking = pd.concat([smoking_inside_data, smoking_inside_data1], ignore_index=True)
smoking  = smoking.fillna(value=0)

# Spraying
filename = '011Spray-2018-02-16-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data1 = pd.read_csv(data, delimiter = ',')
filename = '018Spray-2018-03-01.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data2 = pd.read_csv(data, delimiter = ',')
filename = '019Spray-2018-02-28.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data3 = pd.read_csv(data, delimiter = ',')
spraying = pd.concat([data1, data2, data3], ignore_index=True)
spraying = spraying.fillna(value=0)

# Indoor Clean
filename = '001Indoor-Hoover-Candle-2018-02-06-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data1 = pd.read_csv(data, delimiter = ',')
data1 = data1[(data1['label'] == 0) & (data1['bin0'] < 100)]
filename = '002Indoor-Outdoor-2018-02-06-labeled.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data2 = pd.read_csv(data, delimiter = ',')
data2 = data2[(data2['label'] == 0) & (data2['bin0'] < 100)]
filename = '013Indoor-Day-2018-02-26.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data3 = pd.read_csv(data, delimiter = ',')
filename = '014Indoor-Night-2018-02-26.csv'
data = os.path.join(os.getcwd(), 'api_vlad/data/new/', filename)
data4 = pd.read_csv(data, delimiter = ',')
indoor = pd.concat([data1, data2, data3, data4], ignore_index=True)[:700]
indoor = indoor.fillna(value=0)

bins = ['bin' + str(x) for x in range(15)]
data = pd.DataFrame(pd.concat([indoor, smoking, frying, spraying, candle, boiling], ignore_index=True))[bins]
data = data.fillna(value=0)
labels = [0] * len(indoor) + [6] * len(smoking) + [2] * len(frying) + [7] * len(spraying) + [5] * len(candle) + [3] * len(boiling) 

polltion_sources_classifier = RandomForestClassifier(n_estimators = 50)
polltion_sources_classifier.fit(data, labels)
