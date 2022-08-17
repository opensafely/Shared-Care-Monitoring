import pandas as pd
import numpy as np
import json
from utilities import *
import pathlib


tests = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "levothyroxine", "medication", "region", "rural_urban", "serious_mental_illness", "sex", "bp", "fbc", "lft", "u_e"]


#Make new directory for redacted output
pathlib.Path(OUTPUT_DIR / "rounded").mkdir(parents=True, exist_ok=True)


for test in tests:
    
    if test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication", "region", "rural_urban", "serious_mental_illness", "sex"]:
        
        #Load a df
        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{test}_rate.csv",
            parse_dates=["date"],
         )

        #Apply redaction function
        df_out = redact_round_table(df, "all_sc_overdue_monitoring_num", "population")

        #Output new dataframe with redacted values as a new table
        df_out.to_csv(
            OUTPUT_DIR / f"rounded/redacted_{test}.csv",
            index=False,
        )
    
    if test in ["u_e", "fbc", "lft", "bp"]:

        #Load a df
        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_{test}_overdue_rate.csv",
            parse_dates=["date"],
        )
        
        #Apply redaction function
        df_out = redact_round_table(df, f"{test}_overdue_num", "population")

        #Output new dataframe with redacted values as a new table
        df_out.to_csv(
            OUTPUT_DIR / f"rounded/redacted_{test}.csv",
            index=False,
        )
         
    if test in ["levothyroxine"]:

        #Load a df
        df = pd.read_csv(
            OUTPUT_DIR / f"measure_{test}_overdue_rate.csv",
            parse_dates=["date"],
        )
        
        #Apply redaction function
        df_out = redact_round_table(df, f"{test}_overdue_num", "population")

        #Output new dataframe with redacted values as a new table
        df_out.to_csv(
            OUTPUT_DIR / f"rounded/redacted_{test}.csv",
            index=False,
        )