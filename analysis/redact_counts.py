import pandas as pd
import numpy as np
import json
from utilities import *
import pathlib


measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex"]


#Make new directory for redacted output
pathlib.Path(OUTPUT_DIR / "rounded").mkdir()


for measure in measures:
    
    #Load a df
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",
        parse_dates=["date"],
     )

    #Apply redaction function
    df_out = redact_round_table(df)
    
    #Output new dataframe with redacted values as a new table
    df_out.to_csv(
        OUTPUT_DIR / f"rounded/redacted_{measure}.csv",
    )