import csv

from django.core.management.base import BaseCommand, CommandError
from api_mihai.models import CollectedData


class Command(BaseCommand):
	help = 'Imports the CSV file from the collected data to the database'

	def add_arguments(self, parser):
		parser.add_argument('file_name', type=str)

	def handle(self, *args, **options):

		bin_vals = ['bin'+str(num) for num in range(0,16)]

		with open(options['file_name'], 'rt') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
			for row in reader:

				if row['temperature'] == "" or row['humidity'] == "":
					continue

				feature = CollectedData(
					phone_timestamp=row['phoneTimestamp'],
					pm1=float(row['pm1']),
					pm2_5=float(row['pm2_5']),
					pm10=float(row['pm10']),
					temperature=float(row['temperature']),
					humidity=float(row['humidity']),
					latitude=float(row['gpsLatitude']),
					longitude=float(row['gpsLongitude']),
					altitude=float(row['gpsAltitude']),
					accuracy=float(row['gpsAccuracy']),
					total=row['total'],
					time=row['time'],
				)

				for val in bin_vals:
					setattr(feature, val, row[val])
				# save newly created feature
				feature.save()
