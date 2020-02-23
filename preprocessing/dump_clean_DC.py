import pandas as pd
import datetime

# from pandas.api.types import CategoricalDtype
from paths import DC_W_PATH


DC = pd.read_csv(DC_W_PATH)

median_hum_dc = DC.humidity.median()
list_hum_binary_dc = []
for i in DC["humidity"]:
    if i > median_hum_dc:
        list_hum_binary_dc.append(1)
    else:
        list_hum_binary_dc.append(0)
DC["hum_binary"] = list_hum_binary_dc

DC["datetime"] = pd.to_datetime(DC.datetime)
DC["Day"] = DC.datetime.dt.weekday_name

aver_hum_dc = (
    DC.groupby(["Day", "hum_binary"]).sum() / DC.groupby(["Day", "hum_binary"]).count()
)


# aver_hum_dc['count'].plot(
#    kind='bar', width=0.85)
# plt.xticks(rotation=45)
# plt.show()


# Save to pickled file
DC.to_pickles("pickled_data/DC_df.pickled")

#
#import matplotlib.dates as mdates
#import matplotlib.pylab as plt
#
#DC_f = DC[["temp", "humidity", "windspeed", "workingday"]]
#dc_per_day = DC_f.groupby([DC["datetime"].dt.date]).mean()
#dc_per_day["count"] = DC["count"].groupby([DC["datetime"].dt.date]).sum()
#dc_per_day.rename(
#    columns={"humidity": "hum", "windspeed": "wind", "workingday": "is_workday"},
#    inplace=True,
#)
#dc_per_day["count"].plot()
#fig = plt.figure(dpi=120, figsize=(50, 30))
#ax = (
#    dc_per_day["count"]
#    .loc[
#        (dc_per_day.index > datetime.datetime.strptime("2011-03-01", "%Y-%m-%d").date())
#        & (
#            dc_per_day.index
#            <= datetime.datetime.strptime("2012-06-01", "%Y-%m-%d").date()
#        )
#    ]
#    .plot(x_compat=True)
#    
#)
#    
#dc_per_day = DC.groupby([DC["datetime"].dt.date]).mean()
#dc_per_day["count"] = (DC["count"].groupby([DC["datetime"].dt.date]).sum())    
#d_index = print(dc_per_day.index)
    
#ax.xaxis.set_major_locator(mdates.DayLocator())
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
#plt.show()
