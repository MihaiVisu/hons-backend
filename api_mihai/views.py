from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from .serializers import GeoJsonSerializer
from .classifiers import KmeansClassifier


# view for retrieving midday meadows walking data
def labelled_midday_bins(request):
	serializer = GeoJsonSerializer()
	classifier = KmeansClassifier()
	# remove bin0 outliers
	bin_vals = ['bin'+str(x) for x in range(0,16)]
	features = CollectedData.objects.filter(dataset__name="Walking Meadows Data Midday").filter(bin0__gt=0).filter(bin0__lt=450)
	clusters = classifier.get_environment_clusters(features, 80, bin_vals)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)


# view for retrieving afternoon meadows walking data
def labelled_afternoon_bins(request):
	serializer = GeoJsonSerializer()
	classifier = KmeansClassifier()
	# remove bin0 outliers
	bin_vals = ['bin'+str(x) for x in range(0,16)]
	features = CollectedData.objects.filter(dataset__name="Walking Meadows Data Afternoon").filter(bin0__gt=0).filter(bin0__lt=450)
	clusters = classifier.get_environment_clusters(features, 80, bin_vals)
	return JsonResponse(
		serializer.serialize(CollectedData, features, clusters)
	)
