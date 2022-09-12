import pandas as pd
import numpy as np
import json
from utilities import *

measures = ["bp", "fbc", "lft", "u_e"]

data = []
    
for measure in measures:
    
    #Load a df
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_{measure}_overdue_rate.csv",
        
        parse_dates=["date"],
     )

    #Create column for 'test_type', and assign the name of the relevant test type as data within each of its rows
    df["test_type"] = measure
    
    #Append data frame to list of data
    data.append(df)

#Merge data frames from data list
joined_data = pd.concat(data)

#Output joined data                   
joined_data.to_csv(
        OUTPUT_DIR / f"redacted_test_type.csv",
    )