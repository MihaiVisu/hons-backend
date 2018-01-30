import json
import sys


class GeoJsonSerializer(object):
	def __init__(self):
		self.__features = {
			"type": "FeatureCollection",
			"features": []
		}

	def serialize(self, model, data, labels):
		for obj, label in zip(data, labels):
			self.__features['features'].append(self.__create_feature(model, obj, label))
		return self.__features

	@staticmethod
	def __create_feature(model, obj, label):
		properties = {}
		for attr in model._meta.get_fields():
			if attr.name == 'dataset':
				continue
			elif attr.name == 'latitude':
				latitude = getattr(obj, attr.name)
			elif attr.name == 'longitude':
				longitude = getattr(obj, attr.name)
			else:
				properties[attr.name] = getattr(obj, attr.name)
			properties['label'] = str(label)
		feature = {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": [longitude, latitude],
			},
			"properties": properties
		}
		return feature
	