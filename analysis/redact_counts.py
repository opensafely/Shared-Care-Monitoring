import pandas as pd
import numpy as np
import json
from utilities import *


#Define redaction function
def redact_round_table(df_in):
    """Redacts counts <= 7 and rounds counts to nearest 5"""
    df_out = df_in.where(df_in > 7, np.nan).apply(lambda x: 5 * round(x/5))
    return df_out


measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication" "region", "rural_urban", "serious_mental_illness", "sex"]

for measure in measures:
    
    #Load a df
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",
        parse_dates=["date"],
     )

    #Apply redaction function
    redact_round_table(df)
    
    #Output new dataframe with redacted values as a new table
    df_out.to_csv(
        OUTPUT_DIR / f"redacted_{measure}.csv",
    )

    
#Load population df
df = pd.read_csv(
    OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_rate.csv",        
    parse_dates=["date"],
)
          
#Output new dataframe with redacted values as a new table
df_out.to_csv(
    OUTPUT_DIR / f"redacted_population.csv", index=False
)