import pandas as pd
import numpy as np
import json
from utilities import *


measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex"]

for measure in measures:
     
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",        #load a df
        parse_dates=["date"],
     )

    #Identify monitoring rate in Feb20 and May20, for all categories within each measure 
    feb20 = df.loc[(df["date"]=="2020-03-01"), [measure, "value"]].set_index(measure)
    may20 = df.loc[(df["date"]=="2020-06-01"), [measure, "value"]].set_index(measure)
        
    feb20tomay20_change = may20 - feb20
        
    df = pd.DataFrame(feb20tomay20_change.index.values)
        
    #Output new dataframe with calculated values as a new table
    df.to_csv(
        OUTPUT_DIR / f"joined/changes_{measure}.csv",
    )