import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

import pydeck as pdk

#0. Functions
from function import weather_data_fetch

def convert_df(df):
     return df.to_csv().encode('utf-8')

#1. Layout---------------------------------
#Title
st.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Weather data access</b>', unsafe_allow_html=True)

st.sidebar.title("Location information")

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
st.download_button('Download ' + str(year) + " weather data - " + str(name_station), csv_cdd, str(year) + " weather data - " + str(name_station), 'text/csv', key = "download-csv")

#Plots map
df_map = pd.DataFrame({"lat":[stat_lat, option_0_lat], "lon":[stat_lon, option_0_lon]})
st.map(df_map)


df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))
