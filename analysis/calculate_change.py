import pandas as pd
import numpy as np
import json
from utilities import *

measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex"]

for measure in measures:
    
    #Load a df
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",
        parse_dates=["date"],
     )

    #Identify monitoring rate in Feb20 and May20, for all categories within each measure 
    feb20 = df.loc[(df["date"]=="2020-03-01"), [measure, "value"]].set_index(measure)
    may20 = df.loc[(df["date"]=="2020-06-01"), [measure, "value"]].set_index(measure)
    
    #Calculate change in rates between columns for Feb and May data 
    feb20tomay20_change = may20 - feb20
    
    #Create new dataframe which contains calculated values
    df = pd.DataFrame(feb20tomay20_change, feb20tomay20_change.index.values)

    #Output new dataframe with calculated values as a new table
    df.to_csv(
        OUTPUT_DIR / f"changes_{measure}.csv",
    )
                    

#Load population df
df = pd.read_csv(
    OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_rate.csv",        
    parse_dates=["date"],
)
    
#Identify value ranges for population in Feb20        
feb20_population = df.loc[(df["date"]=="2020-03-01"),"value"].values

#Identify value ranges for population in May20
may20_population = df.loc[(df["date"]=="2020-06-01"),"value"].values 
 
#Calculate change between rates at relevant dates for population
feb20tomay20_change_population = may20_population - feb20_population
        
#Create new dataframe which contains calculated values
df = pd.DataFrame(feb20tomay20_change_population, columns=['value'])
        
#Output new dataframe with calculated values as a new table
df.to_csv(
    OUTPUT_DIR / f"changes_population.csv", index=False
)