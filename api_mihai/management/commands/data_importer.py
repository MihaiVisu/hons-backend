import csv

from django.core.management.base import BaseCommand, CommandError
from api_mihai.models import CollectedData


class Command(BaseCommand):
	help = 'Imports the CSV file from the collected data to the database'

	def add_arguments(self, parser):
		parser.add_argument('file_name', type=str)
		parser.add_argument('dataset', type=int)

	def handle(self, *args, **options):

		bin_vals = ['bin'+str(num) for num in range(0,16)]

		with open(options['file_name'], 'rt') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
			for row in reader:

				if row['temperature'] == "" or row['humidity'] == "":
					continue

				transport_label_id = None
				if 'environment_index' in row.keys():
					transport_label_id = row['environment_index']

				altitude = None
				if 'gpsAltitude' in row.keys():
					if row['gpsAltitude']:
						altitude = float(row['gpsAltitude'])

				motion = 0.0
				lux_level = 0.0
				time = None
				accuracy = None

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
					phone_timestamp=row['phoneTimestamp'],
					pm1=float(row['pm1']),
					pm2_5=float(row['pm2_5']),
					pm10=float(row['pm10']),
					temperature=float(row['temperature']),
					humidity=float(row['humidity']),
					latitude=float(row['gpsLatitude']),
					longitude=float(row['gpsLongitude']),
					altitude=altitude,
					accuracy=accuracy,
					total=row['total'],
					time=time,
					dataset_id=options['dataset'],
					motion=motion,
					lux_level=lux_level,
					transport_label_id=transport_label_id,
				)

				for val in bin_vals:
					setattr(feature, val, row[val])
				# save newly created feature
				feature.save()
