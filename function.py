def degree_analysis(df, base_temp = 18, analysis = "D", output_summary = "M", max_min_diff = True):
    """
    Receives a time series hourly data frame (index must be time) with a temperature value only column.
    Inputs are:
        df: time series data frame
        base_temp: The base temperature of the analysis
        analysis: D for CDD & HDD, H for CDH & HDH
        output_summary: results will be aggregated/aggregated according to the this input
        max_min_diff: method for estimating the mean temperature of the day
    
    """
    #Variable names
    temp_name = df.columns[0]
    CD_name = "CD" + analysis
    HD_name = "HD" + analysis
    
    #Resamplers
    df_cdd = df[temp_name].resample(analysis).agg(["mean", "min", "max"])
    
    #CDD estimations
    if max_min_diff == True:
        df_cdd[CD_name] = df_cdd.apply(lambda x: max(((x["max"]+x["min"])/2)-base_temp,0), axis = 1)
    
    if max_min_diff == False:
        df_cdd[CD_name] = df_cdd.apply(lambda x: max(x["mean"]-base_temp,0), axis = 1)
        
    #HDD estimations
    if max_min_diff == True:
        df_cdd[HD_name] = df_cdd.apply(lambda x: max((base_temp - (x["max"]+x["min"])/2),0), axis = 1)
    
    if max_min_diff == False:
        df_cdd[HD_name] = df_cdd.apply(lambda x: max(base_temp - x["mean"],0), axis = 1)
    
    #Returns result
    return df_cdd.resample(output_summary).agg({"mean":"mean", "min":"min", "max":"max", CD_name:"sum", HD_name:"sum"})


def weather_data_fetch(start, end, lat, lon):
    from meteostat import Stations
    from datetime import datetime
    from meteostat import Hourly

    # Set time period
    start = datetime(2021, 1, 1)
    end = datetime(2021, 12, 31, 23, 59)

    # Gets closest station ID
    stations = Stations()
    stations = stations.nearby(lat, lon)
    station = stations.fetch(1)

            #ID of the closest station
    ID = station.index.values.astype(int)[0]

    # Get hourly data
    data = Hourly(ID, start, end)
    data = data.fetch()

    data
