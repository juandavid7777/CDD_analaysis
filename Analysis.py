import pandas as pd
import numpy as np
import datetime

#Imports file ----------------------------
path_file = "Dubai_Intl_Airp_Meteonorm.csv"

# path_file = "ARE_Abu.Dhabi.412170_IWECEPW.csv"
df_raw = pd.read_csv(path_file, header = 0, parse_dates = ["Date"], dayfirst = True)

#Creates a date time column to be indexed
year = 2022
df_raw["datetime"] = df_raw.apply(lambda x : datetime.datetime(year, x["Date"].month, x["Date"].day, int(x["HH:MM"].split(":")[0])) if int(x["HH:MM"].split(":")[0]) < 24 else datetime.datetime(year, x["Date"].month, x["Date"].day, 0), axis = 1)

#Creates a timeseries dataframe only with temperature
df = df_raw[["datetime","Dry Bulb Temperature {C}"]].set_index("datetime")

#Runs analysis function -----------------------
analysis = "D"

df_cdd = degree_analysis(df,
                base_temp = 18,
                analysis = analysis,
                output_summary = "M",
                max_min_diff = True)


#Plots ---------------------------------------

df_cdd[["CD"+analysis,"HD"+analysis, "mean"]].plot()
