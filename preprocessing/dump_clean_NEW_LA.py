import pandas as pd
#import matplotlib as plt
from pandas.api.types import CategoricalDtype
from paths import la_19_q3
from paths import la_19_q2
from paths import la_19_q1
from paths import la_18_q4
from paths import la_18_q3
from paths import la_18_q2
from paths import la_18_q1
from paths import la_17_q4
from paths import la_17_q3
from paths import la_17_q2
from paths import la_17_q1

#Load dataframes
LA_19_q3 = pd.read_csv(la_19_q3)
LA_19_q2 = pd.read_csv(la_19_q2)
LA_19_q1 = pd.read_csv(la_19_q1)
LA_18_q4 = pd.read_csv(la_18_q4)
LA_18_q3 = pd.read_csv(la_18_q3)
LA_18_q2 = pd.read_csv(la_18_q2)
LA_18_q1 = pd.read_csv(la_18_q1)
LA_17_q4 = pd.read_csv(la_17_q4)
LA_17_q3 = pd.read_csv(la_17_q3)
LA_17_q2 = pd.read_csv(la_17_q2)
LA_17_q1 = pd.read_csv(la_17_q1)

# conacat all dates
frames = [LA_19_q3,LA_19_q2,LA_19_q1,LA_18_q4,LA_18_q3,LA_18_q2,LA_18_q1,LA_17_q4,LA_17_q3,LA_17_q2,LA_17_q1]
LA = pd.concat(frames)

#Drop null values
LA.drop(columns=['bike_type','end_lat','end_lon','end_station','end_station_id','plan_duration',\
                'start_lat','start_lon','start_station','start_station_id'], inplace=True)

#Convert data types
LA['start_time'] = pd.to_datetime(LA.start_time)

#New features
LA['Day'] = LA.start_time.dt.weekday_name
LA['Month'] =  LA.start_time.dt.month_name()

days_of_the_week = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
LA['Day'] = LA['Day'].astype(CategoricalDtype(categories=days_of_the_week, ordered=True))


#PLOTS
#LA.groupby('Day')['duration'].mean().plot(
#    kind='bar', color='r', width=0.85)
#plt.xticks(rotation=45)
#plt.show()
#
#
#LA.groupby('Month')['duration'].count().plot(
#    kind='bar', color='m', width=0.85)
#plt.xticks(rotation=45)
#plt.show()


# Save to pickled file
LA.to_pickle("../pickled_data/LA_new_df.pickled")