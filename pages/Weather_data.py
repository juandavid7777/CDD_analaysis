import streamlit as st

from meteostat import Hourly
from meteostat import Stations

from datetime import datetime


#0. Functions
from function import degree_analysis
from function import weather_data_fetch

def convert_df(df):
     return df.to_csv().encode('utf-8')

#1. Layout---------------------------------
#Title
st.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Weather data access</b>', unsafe_allow_html=True)

st.sidebar.title("Analysis parameters")

option_0_lat = number = st.sidebar.number_input('Latitude', value = 25.2048 )
option_0_lon = number = st.sidebar.number_input('Longitude', value = 55.2708)
option_0_year = number = st.sidebar.number_input('Year', min_value = 2018, max_value=2022, value = 2021)

#3. Creates a date time column to be indexed
year = int(option_0_year)
start = datetime(year, 1, 1)
end = datetime(year, 12, 31, 23, 59)


df_raw = weather_data_fetch(start, end, option_0_lat, option_0_lon)[0]
name_station = weather_data_fetch(start, end, option_0_lat, option_0_lon)[1]

stat_lat = weather_data_fetch(start, end, option_0_lat, option_0_lon)[2]
stat_lon = weather_data_fetch(start, end, option_0_lat, option_0_lon)[3]


#Converts and uploads files
csv_cdd = convert_df(df_raw)
st.download_button('Download ' + str(year) + " weather date - " + str(name_station), csv_cdd, str(year) + " weather date - " + str(name_station), 'text/csv', key = "download-csv")


