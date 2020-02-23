import pandas as pd
from pandas.api.types import CategoricalDtype

# import matplotlib.pyplot as plt
from paths import AUSTIN_ALL_TRIPS_PATH
from paths import AUSTIN_WEATHER
from utils import FtoC, MtoK, to_float

austin_all_trips_df = pd.read_csv(AUSTIN_ALL_TRIPS_PATH)
# austin_stations_df = pd.read_csv(
#     './data/austin-bike/austin_bikeshare_stations.csv', parse_dates=True)


austin_weather = pd.read_csv(AUSTIN_WEATHER)

austin_all_trips_df.start_time = pd.to_datetime(
    austin_all_trips_df.start_time, infer_datetime_format=True
)


# remove null values
austin_all_trips_df.drop(
    columns=["start_station_id", "end_station_id", "month", "year"], inplace=True
)
austin_all_trips_df.dropna(inplace=True)


# convert data types
austin_all_trips_df["start_time"] = pd.to_datetime(austin_all_trips_df.start_time)
austin_all_trips_df["Start_Day"] = austin_all_trips_df.start_time.dt.weekday_name
austin_all_trips_df["Month"] = austin_all_trips_df.start_time.dt.month_name()


# reorder days of the week
days_of_the_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
austin_all_trips_df["Start_Day"] = austin_all_trips_df["Start_Day"].astype(
    CategoricalDtype(categories=days_of_the_week, ordered=True)
)

# Add is_workday feature
us_federal_holidays = [
    "2013-12-25",
    "2013-12-26",
    "2014-12-25",
    "2014-12-26",
    "2015-12-25",
    "2015-12-26",
    "2016-12-25",
    "2016-12-26",
    "2014-01-01",
    "2015-01-01",
    "2016-01-01",
    "2017-01-01",
    "2014-01-20",
    "2015-01-19",
    "2016-01-18",
    "2017-01-16",
    "2014-02-17",
    "2015-02-16",
    "2016-01-15",
    "2014-11-11",
    "2015-11-11",
    "2016-11-11",
    "2017-11-11",
    "2014-07-04",
    "2015-07-04",
    "2016-07-04",
    "2017-07-04",
    "2014-09-01",
    "2015-09-07",
    "2016-09-02",
    "2017-09-04",
    "2014-11-27",
    "2015-11-26",
    "2016-11-24",
    "2017-11-23",
    "2014-11-28",
    "2015-11-27",
    "2016-11-25",
    "2017-11-24",
    "2014-05-26",
    "2015-05-25",
    "2016-05-30",
    "2017-05-29",
    "2014-05-01",
    "2015-05-01",
    "2016-05-01",
    "2017-05-01",
]
working_days = []
for index, row in austin_all_trips_df.iterrows():
    if (
        row["Start_Day"] in ["Saturday", "Sunday"]
        or row["start_time"].strftime("%Y-%m-%d") in us_federal_holidays
    ):
        working_days.append(0)
    else:
        working_days.append(1)
austin_all_trips_df["is_workday"] = working_days

# plot_1:
# austin_all_trips_df.groupby('Start_Day')['duration_minutes'].mean().plot(
#    kind='bar', color='r', width=0.85)
# plt.xticks(rotation=45)
# plt.show()


# plot_2:
# austin_all_trips_df.groupby('Month')['duration_minutes'].count().plot(kind='barh', color='m', width=0.85)
# plt.xticks(rotation=45)
# plt.show()

######
# Clean weather dataset
######
# Datatypes
austin_weather.HumidityAvgPercent = austin_weather.HumidityAvgPercent.map(to_float)
austin_weather.WindAvgMPH = austin_weather.WindAvgMPH.map(to_float)
austin_weather.TempAvgF = austin_weather.TempAvgF.map(to_float)
austin_weather.DewPointAvgF = austin_weather.DewPointAvgF.map(to_float)
# Convert relevant to metric system
austin_weather["TempAvgC"] = austin_weather["TempAvgF"].map(FtoC)
austin_weather["DewPointAvgC"] = austin_weather["DewPointAvgF"].map(FtoC)
austin_weather["WindAvgKmH"] = austin_weather["WindAvgMPH"].map(MtoK)
# austin_weather['VisibilityAvgKm'] = austin_weather['VisibilityAvgMiles'].map(MtoK)


# Create merged df
austin_weather["dateasdatetime"] = pd.to_datetime(austin_weather["Date"]).dt.date
austin_all_trips_df["start_date"] = austin_all_trips_df.start_time.dt.date
austin_all = pd.merge(
    austin_all_trips_df,
    austin_weather,
    left_on="start_date",
    right_on="dateasdatetime",
    how="left",
    sort=False,
)


# Save to pickled file
austin_all_trips_df.to_pickle("../pickled_data/austin_df.pickled")
austin_all.to_pickle("../pickled_data/austin_all.pickled")
