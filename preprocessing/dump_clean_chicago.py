import pandas as pd
from pandas.api.types import CategoricalDtype

from paths import CHICAGO_q1_PATH
from paths import CHICAGO_q2_PATH
from paths import CHICAGO_q3_PATH
from paths import CHICAGO_q4_PATH


chicago_q1 = pd.read_csv(CHICAGO_q1_PATH)
chicago_q2 = pd.read_csv(CHICAGO_q2_PATH)
chicago_q3 = pd.read_csv(CHICAGO_q3_PATH)
chicago_q4 = pd.read_csv(CHICAGO_q4_PATH)


frames = [chicago_q1, chicago_q2, chicago_q3, chicago_q4]
chicago_all_trips_df = pd.concat(frames)

# Remove null values
chicago_all_trips_df.drop(columns=["gender", "birthyear"], inplace=True)

# convert data types
chicago_all_trips_df.tripduration = [
    float(x.replace(",", "")) for x in chicago_all_trips_df.tripduration
]
chicago_all_trips_df["start_time"] = pd.to_datetime(chicago_all_trips_df.start_time)
chicago_all_trips_df["end_time"] = pd.to_datetime(chicago_all_trips_df.end_time)

# add new features - Start_Day & End_Day
chicago_all_trips_df["Day"] = chicago_all_trips_df.start_time.dt.weekday_name

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
chicago_all_trips_df["Day"] = chicago_all_trips_df["Day"].astype(
    CategoricalDtype(categories=days_of_the_week, ordered=True)
)


# Save to pickled file
chicago_all_trips_df.to_pickle("pickled_data/chicago_trips_df.pickled")
