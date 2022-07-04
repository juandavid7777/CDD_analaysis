import streamlit as st

import pandas as pd
import numpy as np
import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots


#0. Functions
from function import degree_analysis

def convert_df(df):
     return df.to_csv().encode('utf-8')

#1. Layout---------------------------------
#Title
st.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Cooling and heating degree analysis</b>', unsafe_allow_html=True)

st.write("Degree days are essentially a simplified representation of outside-air-temperature data. They are widely used for calculations relating to the effect of outside air temperature on building energy consumption. Heating degree days, or HDD, are a measure of how much (in degrees), and for how long (in days), outside air temperature was lower than a specific base temperature (or balance point). They are used for calculations relating to the energy consumption required to heat buildings. Cooling degree days, or CDD, are a measure of how much (in degrees), and for how long (in days), outside air temperature was higher than a specific base temperature. They are used for calculations relating to the energy consumption required to cool buildings. Taken from https://www.degreedays.net/")

#2. Inputs options ----------------------------
st.sidebar.title("Analysis parameters")

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


uploaded_files = st.file_uploader("Choose a CSV file(s)", accept_multiple_files=True)
for uploaded_file in uploaded_files:


     #Inputs for file
     df_raw = pd.read_csv(uploaded_file, header = 0, parse_dates = ["Date"], dayfirst = True)

     #3. Creates a date time column to be indexed
     year = 2022
     df_raw["datetime"] = df_raw.apply(lambda x : datetime.datetime(year, x["Date"].month, x["Date"].day, int(x["HH:MM"].split(":")[0])) if int(x["HH:MM"].split(":")[0]) < 24 else datetime.datetime(year, x["Date"].month, x["Date"].day, 0), axis = 1)

     #Creates a timeseries dataframe only with temperature
     df = df_raw[["datetime","Dry Bulb Temperature {C}"]].set_index("datetime")

     #4. Runs analysis function -----------------------
     analysis = option2[0]

     df_cdd = degree_analysis(df,
                        base_temp = option1,
                        analysis = analysis,
                        output_summary = option3[0],
                        max_min_diff = mean_method)

     #Converts and uploads files
     csv_cdd = convert_df(df_cdd)

     st.download_button('Download ' + option3 + ' D'+ analysis + ' - ' + uploaded_file.name, csv_cdd, option3 + ' D'+ analysis + '_' + uploaded_file.name, 'text/csv', key = "download-csv")


