import urllib
import os
import csv

import numpy as np

from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers

from sklearn.cross_validation import KFold
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier
from .classifiers import classifiers_dict


def get_training_accuracy_mixed_models(estimator, x_trs, y_tr, x_tss, y_ts):
	labels_idx = np.array([0, 1, 2, 3, 4, 6])
	probs_array = np.empty((len(x_tss), x_tss[0].shape[0], len(np.unique(y_tr))))

	for estimator_idx, x_tr in enumerate(x_trs):
		estimator.fit(x_tr, y_tr)
		probs_array[estimator_idx] = estimator.predict_proba(x_tss[estimator_idx])

	final_labels = labels_idx[np.argmax(np.mean(probs_array, axis=0), axis=1)]
	score = accuracy_score(y_ts, final_labels, normalize=True)

	return score, final_labels


@csrf_exempt
def upload_file(request):
	if request.method == 'POST':
		dataset_name = request.POST.get('dataset')

		try:
			dataset_obj = Dataset.objects.get_or_create(name=dataset_name)[0]

			with open('media/file.csv', 'wb') as destination:
				for chunk in request.FILES.get('upload_file', False).chunks():
					destination.write(chunk)

			with open('media/file.csv', 'rt') as csvfile:
				reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
				bin_vals = ['bin'+str(num) for num in range(0,16)]
				for row in reader:

					if row['temperature'] == "" or row['humidity'] == "":
						continue

					transport_label_id = None
					if 'environment_index' in row.keys():
						transport_label_id = row['environment_index']
					else:
						transport_label_id = 0

					altitude = None
					if 'gpsAltitude' in row.keys():
						if row['gpsAltitude']:
							altitude = float(row['gpsAltitude'])

					motion = 0.0
					lux_level = 0.0
					time = None
					accuracy = None
					timestamp = None

					latitude = None
					longitude = None

					# coordinates checking
					if 'gpsLatitude' in row.keys():
						if row['gpsLatitude']:
							latitude = float(row['gpsLatitude'])
					elif 'latitude' in row.keys():
						if row['latitude']:
							latitude = float(row['latitude'])

					if 'gpsLongitude' in row.keys():
						if row['gpsLongitude']:
							longitude = float(row['gpsLongitude'])
					elif 'longitude' in row.keys():
						if row['longitude']:
							longitude = float(row['longitude'])

					# timestamp and other attributes checking
					if 'phoneTimestamp' in row.keys():
						timestamp = row['phoneTimestamp']
					elif 'time' in row.keys():
						timestamp = row['time']
					if 'motion' in row.keys():
						motion = row['motion']
					if 'luxLevel' in row.keys():
						lux_level = row['luxLevel']
					if 'time' in row.keys():
						time = row['time']
					if 'gpsAccuracy' in row.keys():	
						if row['gpsAccuracy']:
							accuracy = float(row['gpsAccuracy'])

					feature = CollectedData(
						phone_timestamp=timestamp,
						pm1=float(row['pm1']),
						pm2_5=float(row['pm2_5']),
						pm10=float(row['pm10']),
						temperature=float(row['temperature']),
						humidity=float(row['humidity']),
						latitude=latitude,
						longitude=longitude,
						altitude=altitude,
						accuracy=accuracy,
						total=row['total'],
						time=time,
						dataset=dataset_obj,
						motion=motion,
						lux_level=lux_level,
						transport_label_id=transport_label_id,
					)

					for val in bin_vals:
						setattr(feature, val, row[val])
					# save newly created feature
					feature.save()

			os.remove('media/file.csv')

		except Exception as e:
			print(e)
			response = 0
	response = 1
	return HttpResponseRedirect('http://localhost:8000/?response={}'.format(response))


def labelled_unsupervised_data(request, 
	dataset_id, 
	number_location_clusters, 
	number_environment_clusters):

	serializer = GeoJsonSerializer()
	classifier = KmeansClassifier()	

	if request.method == "GET":
		attrs = urllib.parse.unquote(request.GET.get('attrs[]')).split(',')
	else:
		attrs = None

	features = CollectedData.objects.order_by('time').filter(
		dataset=dataset_id).filter(
		pm10__gt=0).filter(
		temperature__gt=0).filter(
		bin0__lt=1000).filter(
		humidity__gt=0).filter(
		total__gt=0).filter(
		total__lt=12000)

	clusters = classifier.get_environment_clusters(features, number_location_clusters, attrs, number_environment_clusters)

	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters, {})
	)


def labelled_classified_data(request,
	dataset_id,
	classifier,
	normalise_bin_counts,
	include_urban_environments,
	folds_number):

	serializer = GeoJsonSerializer()

	if request.method == "GET":
		attrs = urllib.parse.unquote(request.GET.get('attrs[]')).split(',')
	else:
		attrs = None

	if folds_number:
		kf = KFold(total_features, n_folds=folds_number, shuffle=True, random_state=0)
		score_array = np.empty(kf.n_folds)

	# apply the outlier removal for pm10 values for the training data
	# according to experiments results
	features = CollectedData.objects.filter(
		dataset=dataset_id).filter(
		pm10__gt=0).filter(
		pm10__lt=450).exclude(
		transport_label_id=7).filter(
		temperature__gt=0).filter(
		total__lt=10000)


	if not folds_number:
		training_inputs = CollectedData.objects.filter(
			dataset__name='Training Data').filter(
			pm10__gt=0).filter(
			pm10__lt=450).exclude(
			transport_label_id=7).filter(
			temperature__gt=0).filter(
			total__lt=10000)

	classifier = classifiers_dict[classifier]

	if classifier == 'mixed_model':
		bin_vals = ['bin'+str(i) for i in range(0,16)]
		attributes_list = [
			bin_vals[8:]+['temperature', 'humidity'],
			bin_vals[:8]+['total']
		]

		if folds_number:
			x_tr1 = np.array(features.values_list(*(attributes_list[0])))
			x_tr2 = np.array(features.values_list(*(attributes_list[1])))
			y_tr = np.array(features.values_list('transport_label', flat=True))
		else:
			x_tr1 = np.array(training_inputs.values_list(*(attributes_list[0])))
			x_tr2 = np.array(training_inputs.values_list(*(attributes_list[1])))
			y_tr = np.array(training_inputs.values_list('transport_label', flat=True))

			x_ts1 = np.array(features.values_list(*(attributes_list[0])))
			x_ts2 = np.array(features.values_list(*(attributes_list[1])))
			y_ts = np.array(features.values_list('transport_label', flat=True))



		if normalise_bin_counts:
			x_tr1[:,:-2] = x_tr1[:,:-2]/np.sum(x_tr1[:,:-2], axis=1).reshape(-1,1)
			x_tr2[:,:-1] = x_tr2[:,:-1]/np.sum(x_tr2[:,:-1], axis=1).reshape(-1,1)
		if include_urban_environments:
			cl = KmeansClassifier()
			clusters = cl.get_environment_clusters(features, 40, attrs, 5)
			x_tr2 = np.append(x_tr2, clusters.reshape(-1,1), axis=1)

	else:

		x_tr = np.array(features.values_list(*attrs))
		y_tr = np.array(features.values_list('transport_label', flat=True))

		if normalise_bin_counts:
			x_tr = x_tr/np.sum(x_tr, axis=1).reshape(-1,1)
		if include_urban_environments:
			cl = KmeansClassifier()
			clusters = cl.get_environment_clusters(features, 40, attrs, 5)
			x_tr = np.append(x_tr, clusters.reshape(-1,1), axis=1)

	total_features = features.count()

	if classifier == 'mixed_model':
		estimator = RandomForestClassifier(random_state=0, n_jobs=-1, n_estimators=260)
		if folds_number:
			for (idx, (train_feature, test_feature)) in enumerate(kf):
				
				score_array[idx], clusters = get_training_accuracy_mixed_models(
					estimator, 
					[x_tr1[train_feature], x_tr2[train_feature]], 
					y_tr[train_feature], 
					[x_tr1[test_feature], x_tr2[test_feature]], 
					y_tr[test_feature]
				)
			accuracy = np.mean(score_array)
		else:
			accuracy, clusters = get_training_accuracy_mixed_models(
					estimator, [x_tr1, x_tr2], y_tr, [x_ts1, x_ts2], y_ts
				)


	else:
		for (idx, (train_feature, test_feature)) in enumerate(kf):
			classifier.fit(x_tr[train_feature], y_tr[train_feature])
			score_array[idx] = classifier.score(x_tr[test_feature], y_tr[test_feature])

		clusters = classifier.predict(x_tr)
		accuracy = np.mean(score_array)

	extras = {
		"score": np.around(accuracy, 2),
		"total_features": total_features
	}

	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters, extras)
	)

def get_datasets(request):
	data = [{'id': obj.pk, 'name': obj.name} for obj in Dataset.objects.all()]
	return JsonResponse(data, safe=False)

def get_attributes(request):
	excluded_fields = [
		'transport_label',
		'dataset',
		'time',
		'accuracy',
		'time',
		'altitude',
		'phone_timestamp',
		'id',
	]

	fields = tuple(map(lambda x: x.name, 
		filter(lambda x: x.name not in excluded_fields, CollectedData._meta.get_fields())))
	return JsonResponse(fields, safe=False)




