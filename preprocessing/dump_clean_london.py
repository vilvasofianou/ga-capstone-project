import pandas as pd
import matplotlib as plt
from pandas.api.types import CategoricalDtype
from paths import LONDON_W_PATH


london_counts = pd.read_csv(LONDON_W_PATH)

london_counts.sort_values(by="timestamp", inplace=True)

london_counts["timestamp"] = pd.to_datetime(london_counts.timestamp)

london_counts["Day"] = london_counts.timestamp.dt.weekday_name

meadian_hum = london_counts.hum.median()
list_hum_binary = []
for i in london_counts["hum"]:
    if i > meadian_hum:
        list_hum_binary.append(1)
    else:
        list_hum_binary.append(0)
london_counts["hum_binary"] = list_hum_binary

sum_london_hum = london_counts.groupby(["Day", "hum_binary"]).sum()
count_london_hum = london_counts.groupby(["Day", "hum_binary"]).count()
aver_hum_london = sum_london_hum / count_london_hum


# PLOT AVERAGE HUM
# aver_hum_london.cnt.plot(
#    kind='barh', width=0.85)
# edw vlepoume oti to humidity otan einai megalo (panw apo to median =1) epireazei to soukou
# pou oi anthrwpoi exoun tin epologi
# enw otan einai mikrotero tou median (=0) oxi

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
london_counts["Day"] = london_counts["Day"].astype(
    CategoricalDtype(categories=days_of_the_week, ordered=True)
)

# Create is_workday feature
london_counts["is_workday"] = (1 - london_counts.is_holiday) * (
    1 - london_counts.is_weekend
)


london_counts.groupby("Day")["cnt"].mean().plot(kind="bar", color="r", width=0.85)
plt.pyplot.xticks(rotation=45)
plt.pyplot.show()


# Save to pickled file
london_counts.to_pickle("pickled_data/london_counts_df.pickled")
