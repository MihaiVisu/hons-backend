import urllib

import numpy as np

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sklearn.cross_validation import KFold
from sklearn.model_selection import train_test_split

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier
from .classifiers import classifiers_dict


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
		pm10__gt=0).filter(pm10__lt=450).filter(temperature__gt=0)

	clusters = classifier.get_environment_clusters(features, number_location_clusters, attrs, number_environment_clusters)

	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)


def labelled_classified_data(request,
	dataset_id,
	classifier,
	validation_criterion,
	folds_number):

	serializer = GeoJsonSerializer()

	if request.method == "GET":
		attrs = urllib.parse.unquote(request.GET.get('attrs[]')).split(',')
	else:
		attrs = None

	# apply the outlier removal for pm10 values for the training data
	# according to experiments results
	features = CollectedData.objects.order_by('time').filter(
		dataset=dataset_id).filter(
		pm10__gt=0).filter(pm10__lt=450).filter(temperature__gt=0)

	classifier = classifiers_dict[classifier]

	x_tr = np.array(features.values_list(*attrs))
	y_tr = np.array(features.values_list('transport_label', flat=True))

	total_features = features.count()

	if validation_criterion == 'kf':
		kf = KFold(total_features, n_folds=folds_number, shuffle=True, random_state=0)
		score_array = np.empty(kf.n_folds)
		for (idx, (train_feature, test_feature)) in enumerate(kf):
			classifier.fit(x_tr[train_feature], y_tr[train_feature])
			score_array[idx] = classifier.score(x_tr[test_feature], y_tr[test_feature])
		accuracy = np.mean(score_array)

	else:
		x_train, x_test, y_train, y_test = train_test_split(x_tr, y_tr, test_size=0.25, random_state=0)
		classifier.fit(x_train, y_train)
		accuracy = classifier.score(x_test, y_test)

	clusters = classifier.predict(x_tr)

	extras = {
		"score": np.around(accuracy, 2),
		"total_features": total_features
	}

	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters, extras)
	)


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





