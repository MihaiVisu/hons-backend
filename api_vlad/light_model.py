import os
import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB

def day_night(data_input):
    latitude = data_input['gpsLatitude']
    longitude = data_input['gpsLongitude']
    date = dt.datetime.fromtimestamp(data_input['phoneTimestamp'] / 1000)

    url = "https://api.sunrise-sunset.org/json?lat=" + str(latitude) + "&lng=" + str(longitude) + "&date=" + str(date)

    response = requests.get(url)

    sunrise = response.json()['results']['sunrise']
    sunrise = dt.datetime.strptime(sunrise, "%I:%M:%S %p").time()

    sunset = response.json()['results']['sunset']
    sunset = dt.datetime.strptime(sunset, "%I:%M:%S %p").time()

    current_time = date.time()

    if current_time < sunrise or current_time > sunset:
        return "Night"
    else:
        return "Day"

data1 = pd.read_csv('api_vlad/data/new/012Outdoor-Night-Day-2018-02-25.csv', delimiter = ',')

outdoor_day = data1[(data1['luxLevel'] > 10) & (data1['luxLevel'] < 400)]['luxLevel']
outdoor_night = data1[data1['luxLevel'] < 10]['luxLevel']

indoor_day = pd.read_csv('api_vlad/data/new/013Indoor-Day-2018-02-26.csv', delimiter = ',')
indoor_day = indoor_day[indoor_day['luxLevel'] > 3]['luxLevel']
indoor_night = pd.read_csv('api_vlad/data/new/014Indoor-Night-2018-02-26.csv', delimiter = ',')
indoor_night = indoor_night['luxLevel']

data_day = pd.DataFrame(pd.concat([outdoor_day, indoor_day], ignore_index=True))
data_night = pd.DataFrame(pd.concat([outdoor_night, indoor_night], ignore_index=True))

labels_day = [1] * len(outdoor_day) + [0] * len(indoor_day)
labels_night = [1] * len(outdoor_night) + [0] * len(indoor_night)

# Naive Bayes
day_classifier = GaussianNB()
day_classifier.fit(data_day, labels_day)

night_classifier = GaussianNB()
night_classifier.fit(data_night, labels_night)