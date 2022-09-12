import pandas as pd
import numpy as np
import json
from utilities import *

measures = ["bp", "fbc", "lft", "u_e"]

for measure in measures:
    
    #Load a df
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_{measure}_overdue_rate.csv",
        
        parse_dates=["date"],
     )


    #Identify monitoring rate in Feb20 and May20, for all categories within each measure 
    data = df.loc[(df[measure, "value"].set_index(measure)
    
    #Create new dataframe which contains extracted values
    df = pd.DataFrame(data.index.values)

    #Output new dataframe with calculated values as a new table, appending as appropriate?
    df.to_csv(
        OUTPUT_DIR / f"changes_test_type.csv",
    )