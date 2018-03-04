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

from api_vlad.pollution_model import polltion_sources_classifier
from api_vlad.light_model import day_classifier, night_classifier, day_night


## Labels:
# 0 - Clean Indoor
# 1 - Outdoor
# 2 - Candle Burning
# 3 - Frying Data
# 4 - Boiling Data

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

@csrf_exempt
def predict_pollution(request):
	response=""
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		print(body['bins'])

		prediction = polltion_sources_classifier.predict(np.array(body['bins']).reshape(1,-1))

		print(prediction[0])

		response = {
			"prediction" : str(prediction[0])
		}

	return HttpResponse(json.dumps(response))	

def test(request):
	return HttpResponse("It works!")

