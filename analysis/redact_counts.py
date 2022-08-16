import pandas as pd
import numpy as np
import json
from utilities import *
import pathlib


measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "levothyroxine", "medication", "region", "rural_urban", "serious_mental_illness", "sex", "bp", "fbc", "lft", "u_e"]


#Make new directory for redacted output
pathlib.Path(OUTPUT_DIR / "rounded").mkdir()


for measure in measures:
    
    if measure in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication", "region", "rural_urban", "serious_mental_illness", "sex"]:
        
        #Load a df
        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",
            parse_dates=["date"],
         )

        #Apply redaction function
        df_out = redact_round_table(df, "all_sc_overdue_monitoring_num", "population")

        #Output new dataframe with redacted values as a new table
        df_out.to_csv(
            OUTPUT_DIR / f"rounded/redacted_{measure}.csv",
        )
    
    if measure in ["u_e"]:

        #Load a df
        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_{measure}_overdue_rate.csv",
            parse_dates=["date"],
        )
        
        #Apply redaction function
        df_out = redact_round_table(df, "u_e_overdue_num", "population")

        #Output new dataframe with redacted values as a new table
        df_out.to_csv(
            OUTPUT_DIR / f"rounded/redacted_{measure}.csv",
        )
        
#TO DO:  "levothyroxine", "fbc", "lft", "bp"