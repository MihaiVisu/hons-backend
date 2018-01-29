from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json

import os
import numpy as np
import pandas as pd
import sklearn as sklearn

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

# initialize paths to csv files
bedroom_data = os.path.join(os.getcwd(), 'api_vlad/data/indoor', 'flat-clean-2018-01-17.csv')
kitchen_data = os.path.join(os.getcwd(), 'api_vlad/data/indoor', 'kitchen-clean-2018-01-21.csv')

candle_data = os.path.join(os.getcwd(), 'api_vlad/data/candle', 'candle-burning-2017-11-20.csv')
frying_data = os.path.join(os.getcwd(), 'api_vlad/data/frying', 'frying-2018-01-20.csv')
boiling_data = os.path.join(os.getcwd(), 'api_vlad/data/boiling', 'boiling-2018-01-23.csv')

outdoor_data1 = os.path.join(os.getcwd(), 'api_vlad/data/outdoor', 'meadows-2017-12-04.csv')
outdoor_data2 = os.path.join(os.getcwd(), 'api_vlad/data/outdoor', 'meadows-2017-12-05.csv')

# load data from csv files to DataFrames
bedroom_data = pd.read_csv(bedroom_data, delimiter = ',')
kitchen_data = pd.read_csv(kitchen_data, delimiter = ',')

candle_data = pd.read_csv(candle_data, delimiter = ',')
frying_data = pd.read_csv(frying_data, delimiter = ',')
boiling_data = pd.read_csv(boiling_data, delimiter = ',')

outdoor_data1 = pd.read_csv(outdoor_data1, delimiter = ',')
outdoor_data2 = pd.read_csv(outdoor_data2, delimiter = ',')


# removing outliers
outdoor_data1 = outdoor_data1[[(x < 400 and x > 0) for x in outdoor_data1['bin0']]]
outdoor_data2 = outdoor_data2[[(x < 400 and x > 0) for x in outdoor_data2['bin0']]]

bedroom_data = bedroom_data[2:]

data = pd.concat([bedroom_data, kitchen_data, outdoor_data1, outdoor_data2, candle_data, frying_data, boiling_data])

## Labels:
# 0 - Clean Indoor
# 1 - Outdoor
# 2 - Candle Burning
# 3 - Frying Data
# 4 - Boiling Data

Y = [0] * 536 + [1] * 486 + [2] * 280 + [3] * 48 + [4] * 103

X = data[['bin' + str(x) for x in range(15)]]
X = X.fillna(value=0)

# split dataset into train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.75, test_size=0.25, random_state=0)


# train ML model
rf = RandomForestClassifier(n_estimators = 50).fit(X_train,Y_train)



@csrf_exempt
def predict(request):
	response=""
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		content = body["data"]
		print(content)

		rf_prediction = rf.predict(content)
		response = {
			"prediction" : str(rf_prediction[0])
		}

	return HttpResponse(json.dumps(response))

def test(request):
	return HttpResponse("It works!")

