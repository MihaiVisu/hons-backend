import csv
import calendar
import datetime

from django.core.management.base import BaseCommand, CommandError
from api_mihai.models import CollectedData


class Command(BaseCommand):
	help = 'Imports the CSV file from the collected data to the database'

	def add_arguments(self, parser):
		parser.add_argument('file_name', type=str)
		parser.add_argument('dataset', type=int)

	# method that converts date in date format from the london data into phoneTimestamp
	# for database records
	@staticmethod
	def __convert_date_to_timestamp(date):
		d = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").utctimetuple()
		return calendar.timegm(d)

	# method that gets time as a string from the date in the format
	# of the london data, for database records
	@staticmethod
	def __get_time_string(date):
	    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").time().strftime("%H:%M:%S")

	def handle(self, *args, **options):
		bin_vals = ['bin'+str(num) for num in range(0,16)]

		with open(options['file_name'], 'rt') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
			for row in reader:

				if row['temperature'] == "" or row['humidity'] == "":
					continue

				timestamp = self.__convert_date_to_timestamp(row['phoneTimestamp'])
				time = self.__get_time_string(row['phoneTimestamp'])

				feature = CollectedData(
					phone_timestamp=timestamp,
					pm1=float(row['pm1']),
					pm2_5=float(row['pm2_5']),
					pm10=float(row['pm10']),
					temperature=float(row['temperature']),
					humidity=float(row['humidity']),
					latitude=float(row['gpsLatitude']),
					longitude=float(row['gpsLongitude']),
					time=time,
					dataset_id=options['dataset'],
					transport_label_id=row['environment_index'],
				)

				for val in bin_vals:
					setattr(feature, val, row[val])
				# save newly created feature
				feature.save()
