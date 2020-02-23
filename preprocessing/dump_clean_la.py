# -*- coding: utf-8 -*-
import pandas as pd
from pandas.api.types import CategoricalDtype
from paths import LA_ALL_TRIPS_PATH


la_trips_df = pd.read_csv(LA_ALL_TRIPS_PATH)
# clean the column names
la_trips_df.columns = [x.replace(' ','_') for x in la_trips_df.columns]

#Remove null values
la_trips_df.drop(columns=['LA_Specific_Plans'], inplace=True)
la_trips_df.dropna(inplace=True)

#convert data types
la_trips_df['Start_Time'] = pd.to_datetime(la_trips_df.Start_Time)
la_trips_df['End_Time'] = pd.to_datetime(la_trips_df.End_Time)

#add new features - Start_Day, End_Day & Month
la_trips_df['Start_Day'] = la_trips_df.Start_Time.dt.weekday_name
la_trips_df['End_Day'] = la_trips_df.End_Time.dt.weekday_name
la_trips_df['Month'] =  la_trips_df.Start_Time.dt.month_name()

#reorder days of the week
days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
la_trips_df['Start_Day'] = la_trips_df['Start_Day'].astype(CategoricalDtype(categories=days_of_the_week, ordered=True))


#Plots will be displayed on EDA:
#la_trips_df.groupby('Start_Day')['Duration'].mean().plot(
#    kind='bar', color='r', width=0.85)
#plt.xticks(rotation=45)
#plt.show()


#la_trips_df.groupby('End_Day')['Duration'].mean().plot(
#    kind='bar', color='r', width=0.85)
#plt.xticks(rotation=45)
#plt.show()

#la_trips_df.groupby('Month')['Duration'].count().plot(
#    kind='bar', color='m', width=0.85)
#plt.xticks(rotation=45)
#plt.show()

# Save to pickled file
la_trips_df.to_pickle("../pickled_data/la_trips_df.pickled")
