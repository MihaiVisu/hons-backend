from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from .serializers.serializers import GeoJsonSerializer


# view for retrieving midday meadows walking data
def labelled_midday(request):
	
	serializer = GeoJsonSerializer()
	features = CollectedData.objects.filter(dataset__name="Walking Meadows Data Midday")

	return JsonResponse(
		serializer.serialize(CollectedData, features)
	)


# view for retrieving afternoon meadows walking data
def labelled_afternoon(request):

	serializer = GeoJsonSerializer()
	features = CollectedData.objects.filter(dataset__name="Walking Meadows Data Afternoon")

	return JsonResponse(
		serializer.serialize(CollectedData, features)
	)
