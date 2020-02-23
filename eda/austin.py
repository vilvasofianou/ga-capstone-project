import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Print all the heads
# file_names = [f for f in glob.glob('./data' + "**/**/*.csv", recursive=True)]
# dataframes = {}
# for file_name in file_names:
#     df = pd.read_csv(file_name)
#     dataframes[file_name] = df
#     print(df.head())

austin_all_trips_df = pd.read_csv(
    './data/austin-bike/austin_bikeshare_trips.csv', parse_dates=True)
austin_all_trips_df.start_time = pd.to_datetime(
    austin_all_trips_df.start_time, infer_datetime_format=True)
austin_date_value_counts = austin_all_trips_df.start_time.dt.date.value_counts()
# austin_date_value_counts.plot()
# plt.show()

austin_date_value_counts_2014 = austin_date_value_counts.filter(
    like='2014').sort_index()
austin_date_value_counts_2015 = austin_date_value_counts.filter(
    like='2015').sort_index()
austin_date_value_counts_2016 = austin_date_value_counts.filter(
    like='2016').sort_index()
# t = linspace(1, 364, 364)
for dvc in [austin_date_value_counts_2014, austin_date_value_counts_2015, austin_date_value_counts_2016]:
    values = dvc.values
    plt.plot(savgol_filter(values / np.mean(values), 21, 3))

# austin_date_value_counts_2015.plot()
# austin_date_value_counts_2016.plot()
plt.show()
# daily_counts_per_year = pd.DataFrame(columns)
