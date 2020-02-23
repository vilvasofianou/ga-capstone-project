import pandas as pd
from pandas.api.types import CategoricalDtype
from paths import SAN_FRAN_TRIPS_PATH, SAN_FRAN_WEATHER_PATH
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import FtoC, MtoK

plt.rcParams["figure.figsize"] = (6, 4)
plt.rcParams["font.size"] = 14
plt.style.use("ggplot")
sns.set(font_scale=1.5)


sf_trips = pd.read_csv(SAN_FRAN_TRIPS_PATH)
sf_weather = pd.read_csv(SAN_FRAN_WEATHER_PATH)
# sf_stations_df = pd.read_csv(
#     './data/sf-bay-area-bike-share/station.csv', parse_dates=True)
# sf_status_df = pd.read_csv(
#     './data/sf-bay-area-bike-share/status.csv', parse_dates=True)
# sf_weather_df = pd.read_csv(
#     './data/sf-bay-area-bike-share/weather.csv', parse_dates=True)


####################
# Clean trips
####################
## Plot outliers
# fig, ax = plt.subplots(figsize=(20, 10))
#
# sns.boxplot(
#    data=sf_trips,
#    orient="h",
#    fliersize=8,
#    linewidth=1.5,
#    notch=True,
#    saturation=0.5,
#    whis=1.5,
#    ax=ax,
# )
s
# Remove NaN values:
sf_trips.drop(columns=["zip_code"], inplace=True)

# Remove outliers of duration column:
sf_trips.drop(sf_trips.index[[573566, 382718, 440339, 371066]], inplace=True)
# green_diamond = dict(markerfacecolor="g", marker="D")
# fig, ax = plt.subplots()
# ax.set_title("Duration outliers removed ")
# ax.boxplot(sf_trips.duration, flierprops=green_diamond)

sf_trips["date"] = sf_trips.start_date.map(lambda x: x.split(" ")[0])

# Change the data-type of start_date & end_date columns to datetime:
sf_trips["start_date"] = pd.to_datetime(sf_trips.start_date)
sf_trips["end_date"] = pd.to_datetime(sf_trips.end_date)

# Creating new features including the day of the week as categories to plot them in order.
sf_trips["Start_Day"] = sf_trips.start_date.dt.weekday_name
sf_trips["End_Day"] = sf_trips.end_date.dt.weekday_name
days_of_the_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
sf_trips["Start_Day"] = sf_trips["Start_Day"].astype(
    CategoricalDtype(categories=days_of_the_week, ordered=True)
)
sf_trips["End_Day"] = sf_trips["End_Day"].astype(
    CategoricalDtype(categories=days_of_the_week, ordered=True)
)


# Create Month feature
sf_trips["Month"] = sf_trips.start_date.dt.month_name()


#####################
# Clean weather
#####################
sf_weather.drop("events", axis=1, inplace=True)
sf_weather.drop("max_gust_speed_mph", axis=1, inplace=True)
sf_weather.dropna(inplace=True)
sf_weather["Datetime"] = pd.to_datetime(sf_weather.date)
sf_weather.set_index("Datetime", inplace=True)
sf_weather = sf_weather.sort_index().resample("D").mean()
sf_weather["date"] = sf_weather.index
sf_weather.date = sf_weather.date.map(lambda x: x.strftime("%-m/%-d/%Y"))
# den exei duplicates
# sf_weather.drop_duplicates(keep='first', inplace=True)

# Convert relevant to metric system
sf_weather["mean_temperature_c"] = sf_weather["mean_temperature_f"].apply(FtoC)
sf_weather["mean_dew_point_c"] = sf_weather["mean_dew_point_f"].apply(FtoC)
sf_weather["mean_visibility_km"] = sf_weather["mean_visibility_miles"].apply(MtoK)
sf_weather["mean_wind_speed_kmh"] = sf_weather["mean_wind_speed_mph"].apply(MtoK)


#######################
# Add workday feature
#######################
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
    "2017-11-24" "2014-05-26",
    "2015-05-25",
    "2016-05-30",
    "2017-05-29",
    "2014-05-01",
    "2015-05-01",
    "2016-05-01",
    "2017-05-01",
]
working_days_sf = []
for index, row in sf_trips.iterrows():
    if (
        row["Start_Day"] in ["Saturday", "Sunday"]
        or row["start_date"].strftime("%Y-%m-%d") in us_federal_holidays
    ):
        working_days_sf.append(0)
    else:
        working_days_sf.append(1)
sf_trips["is_workday"] = working_days_sf

#######################
# Create sf_all merged dataset
#######################
sf_all = pd.merge(
    sf_trips, sf_weather, left_on="date", right_on="date", how="left", sort=False
)
sf_humidity_median = sf_all.mean_humidity.median()
sf_temp_median = sf_all.mean_temperature_f.median()
sf_all["mean_humidity_binary"] = np.nan
sf_all["mean_humidity_binary"][sf_all["mean_humidity"] > sf_humidity_median] = 1
sf_all["mean_humidity_binary"][sf_all["mean_humidity"] < sf_humidity_median] = 0


########################
# Save to pickled files
########################
sf_trips.to_pickle("pickled_data/sf_trips_df.pickled")
sf_weather.to_pickle("pickled_data/sf_weather_df.pickled")
sf_all.to_pickle("pickled_data/sf_all_df.pickled")
