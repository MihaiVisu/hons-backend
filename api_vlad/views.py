from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json

import os
import numpy as np
import pandas as pd
import sklearn as sklearn
import datetime as dt
import requests

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score, log_loss
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

## Labels:
# 0 - Clean Indoor
# 1 - Outdoor
# 2 - Candle Burning
# 3 - Frying Data
# 4 - Boiling Data

data1 = pd.read_csv('api_vlad/data/new/012Outdoor-Night-Day-2018-02-25.csv', delimiter = ',')

outdoor_day = data1[(data1['luxLevel'] > 10) & (data1['luxLevel'] < 400)]['luxLevel']
outdoor_night = data1[data1['luxLevel'] < 10]['luxLevel']

indoor_day = pd.read_csv('api_vlad/data/new/013Indoor-Day-2018-02-26.csv', delimiter = ',')
indoor_day = indoor_day[indoor_day['luxLevel'] > 3]['luxLevel']
indoor_night = pd.read_csv('api_vlad/data/new/014Indoor-Night-2018-02-26.csv', delimiter = ',')
indoor_night = indoor_night['luxLevel']

data_day = pd.DataFrame(pd.concat([outdoor_day, indoor_day], ignore_index=True))
data_night = pd.DataFrame(pd.concat([outdoor_night, indoor_night], ignore_index=True))

labels_day = [1] * len(outdoor_day) + [0] * len(indoor_day)
labels_night = [1] * len(outdoor_night) + [0] * len(indoor_night)

X_train_day, X_test_day, Y_train_day, Y_test_day = train_test_split(data_day, labels_day, train_size=0.75, test_size=0.25, random_state=0)
X_train_night, X_test_night, Y_train_night, Y_test_night = train_test_split(data_night, labels_night, train_size=0.75, test_size=0.25, random_state=0)


# Naive Bayes
clf_day = GaussianNB()
clf_day.fit(X_train_day, Y_train_day)

clf_night = GaussianNB()
clf_night.fit(X_train_night, Y_train_night)

def day_night(data_input):
    latitude = data_input['gpsLatitude']
    longitude = data_input['gpsLongitude']
    date = dt.datetime.fromtimestamp(data_input['phoneTimestamp'] / 1000)

    url = "https://api.sunrise-sunset.org/json?lat=" + str(latitude) + "&lng=" + str(longitude) + "&date=" + str(date)

    response = requests.get(url)

    sunrise = response.json()['results']['sunrise']
    sunrise = dt.datetime.strptime(sunrise, "%I:%M:%S %p").time()

    sunset = response.json()['results']['sunset']
    sunset = dt.datetime.strptime(sunset, "%I:%M:%S %p").time()

    current_time = date.time()

    if current_time < sunrise or current_time > sunset:
        return "Night"
    else:
        return "Day"


@csrf_exempt
def predict(request):
	response=""
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		print(body['luxLevel'])

		if (day_night(body) == "Day"):
			prediction = clf_day.predict(np.array(body['luxLevel']).reshape(1,-1))
		else:
			prediction = clf_night.predict(np.array(body['luxLevel']).reshape(1,-1))

		response = {
			"prediction" : str(prediction[0])
		}

	return HttpResponse(json.dumps(response))

def test(request):
	return HttpResponse("It works!")

