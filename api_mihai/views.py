import urllib

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier


def labelled_unsupervised_data(request, dataset_id):
	serializer = GeoJsonSerializer()
	classifier = KmeansClassifier()

	if request.method == "GET":
		attrs = urllib.parse.unquote(request.GET.get('attrs[]')).split(',')
	else:
		attrs = None

	features = CollectedData.objects.order_by('time').filter(
		dataset_id=dataset_id).filter(
		bin0__gt=0).filter(bin0__lt=450)

	clusters = classifier.get_environment_clusters(features, 80, attrs)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)


def labelled_london_data(request, data_type):
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
		pm10__gt=0).filter(pm10__lt=450)

	if data_type == 'supervised':
		clusters = features.values_list('transport_label_id', flat=True)
	else:
		classifier = KmeansClassifier()
		clusters = classifier.get_environment_clusters(features, 80, attrs)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)
