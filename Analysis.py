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


#2. Inputs file ----------------------------
#path_file = "Dubai_Intl_Airp_Meteonorm.csv"

# path_file = "ARE_Abu.Dhabi.412170_IWECEPW.csv"
#df_raw = pd.read_csv(path_file, header = 0, parse_dates = ["Date"], dayfirst = True)


uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
     df_raw = pd.read_csv(uploaded_file, header = 0, parse_dates = ["Date"], dayfirst = True)

     #3. Creates a date time column to be indexed
     year = 2022
     df_raw["datetime"] = df_raw.apply(lambda x : datetime.datetime(year, x["Date"].month, x["Date"].day, int(x["HH:MM"].split(":")[0])) if int(x["HH:MM"].split(":")[0]) < 24 else datetime.datetime(year, x["Date"].month, x["Date"].day, 0), axis = 1)

     #Creates a timeseries dataframe only with temperature
     df = df_raw[["datetime","Dry Bulb Temperature {C}"]].set_index("datetime")

     #4. Runs analysis function -----------------------
     analysis = "D"

     df_cdd = degree_analysis(df,
                        base_temp = 18,
                        analysis = analysis,
                        output_summary = "M",
                        max_min_diff = True)


     #5. Plots ---------------------------------------
     df_cdd[["CD"+analysis,"HD"+analysis, "mean"]].plot()

     st.write("filename:", uploaded_file.name)

     csv_cdd = convert_df(df_cdd)

     st.download_button('Download CSV', csv_cdd, "file.csv", 'text/csv', key = "download-csv")


