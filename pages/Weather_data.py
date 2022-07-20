import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

from meteostat import Stations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


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


# Gets closest station ID
stations = Stations()
stations = stations.nearby(option_0_lat, option_0_lon)
station = stations.fetch(3)

selected_station = st.sidebar.selectbox( 'Select the weather station', station.name)

selected_lat = station[station.name == selected_station]["latitude"]
selected_lon = station[station.name == selected_station]["longitude"]

# Gets raw data
df_raw = weather_data_fetch(start, end, selected_lat, selected_lon)[0]
name_station = weather_data_fetch(start, end, selected_lat, selected_lon)[1]

stat_lat = weather_data_fetch(start, end, selected_lat, selected_lon)[2]
stat_lon = weather_data_fetch(start, end, selected_lat, selected_lon)[3]


#Converts and uploads files
csv_cdd = convert_df(df_raw)
st.download_button('Download ' + str(year) + " weather data - " + str(name_station), csv_cdd, str(year) + " weather data - " + str(name_station), 'text/csv', key = "download-csv")

#Plots map
list_lat = [option_0_lat]
list_lat.extend(list(station.latitude))

list_lon = [option_0_lon]
list_lon.extend(list(station.longitude))

df_map = pd.DataFrame({"lat": list_lat, "lon": list_lon})
st.map(df_map)

#Plots

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_raw.index,
    y=df_raw["temp"],
    mode = 'lines',
    name = "Temperature (C)",
    # line = dict(width = 1.5, dash = 'solid', color = "cyan"),
    ))

fig.add_trace(go.Scatter(
    x=df_raw.index,
    y=df_raw["rhum"],
    mode = 'lines',
    name = "Relative humidity (%)",
    # line = dict(width = 1.0, color = "cyan")
    ),secondary_y=True)

    #Defines figure properties
fig.update_layout(
    title = "Sample weather data for " + str(name_station) + " - " + str(year),
    xaxis_title= "Date",
    yaxis_title= "Temperature (C)",
    legend_title="Weather",
    xaxis_rangeslider_visible=False)

fig.update_layout(hovermode="x unified")

st.plotly_chart(fig)