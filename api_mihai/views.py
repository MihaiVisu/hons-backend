import urllib

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier


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
	dataset = Dataset.objects.get(name='London Data')
	features = CollectedData.objects.order_by('time').filter(
		dataset=dataset).filter(
		pm10__gt=0).filter(pm10__lt=450).filter(temperature__gt=0)

	clusters = features.values_list('transport_label_id', flat=True)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
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





