import streamlit as st

import pandas as pd
import numpy as np
import datetime
from datetime import datetime

from meteostat import Hourly
from meteostat import Stations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


#0. Functions
from function import degree_analysis
from function import weather_data_fetch

def convert_df(df):
     return df.to_csv().encode('utf-8')

#1. Layout---------------------------------
#Title
st.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Cooling and heating degree analysis</b>', unsafe_allow_html=True)

st.write("Degree days are essentially a simplified representation of outside-air-temperature data. They are widely used for calculations relating to the effect of outside air temperature on building energy consumption. Heating degree days, or HDD, are a measure of how much (in degrees), and for how long (in days), outside air temperature was lower than a specific base temperature (or balance point). They are used for calculations relating to the energy consumption required to heat buildings. Cooling degree days, or CDD, are a measure of how much (in degrees), and for how long (in days), outside air temperature was higher than a specific base temperature. They are used for calculations relating to the energy consumption required to cool buildings. Taken from https://www.degreedays.net/")

#2. Inputs options ----------------------------
st.sidebar.title("Analysis parameters")

option_0_lat = number = st.sidebar.number_input('Latitude', value = 25.2048 )
option_0_lon = number = st.sidebar.number_input('Longitude', value = 55.2708)
option_0_year = number = st.sidebar.number_input('Year', min_value = 2018, max_value=2022)

option1 = st.sidebar.slider('Base temperature (C)', 0.0, 35.0, step = 0.5, value = 18.0)

option2 = st.sidebar.selectbox(
     'Type of analysis?',
     ('Hourly', 'Daily', 'Monthly'), index =1)

option3 = st.sidebar.selectbox(
     'Summary output timeframe',
     ('Hourly', 'Daily', 'Monthly'), index = 2)

option4 = st.sidebar.checkbox('Max - min mean estimation method')
if option4:
     mean_method = True
else:
    mean_method = False


#3. Creates a date time column to be indexed
year = option_0_year
start = datetime(year, 1, 1)
end = datetime(year, 12, 31, 23, 59)

df_raw = weather_data_fetch(start, end, option_0_lat, option_0_lon)[0]
name_station = weather_data_fetch(start, end, option_0_lat, option_0_lon)[1]

#Creates a timeseries dataframe only with temperature
df = df_raw[["temp"]]

#4. Runs analysis function -----------------------
analysis = option2[0]

df_cdd = degree_analysis(df,
                    base_temp = option1,
                    analysis = analysis,
                    output_summary = option3[0],
                    max_min_diff = mean_method)

#Converts and uploads files
csv_cdd = convert_df(df_cdd)

st.download_button('Download ' + str(year) + " " + option3 + ' D'+ analysis + ' - ' + name_station, csv_cdd, option3 + ' D'+ analysis + '_' + str(year) + '_' + name_station, 'text/csv', key = "download-csv")


