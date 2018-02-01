import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier


@csrf_exempt
def labelled_unsupervised_data(request, dataset_id):
	serializer = GeoJsonSerializer()
	classifier = KmeansClassifier()

	attrs = None

	if request.method == "POST":
		attrs = json.loads(request.body.decode('utf-8'))['attrs']

	features = CollectedData.objects.order_by('time').filter(
		dataset_id=dataset_id).filter(
		bin0__gt=0).filter(bin0__lt=450)

	clusters = classifier.get_environment_clusters(features, 80, attrs)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)


def labelled_london_unsupervised(request):
	serializer = GeoJsonSerializer()
