import pandas as pd
import numpy as np
import json
from pathlib import Path
from ebmdatalab import charts
from utilities import (
    OUTPUT_DIR,
    ANALYSIS_DIR,
    plot_measures,
)

for test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication", "region", "rural_urban", "serious_mental_illness", "sex", "bp", "fbc", "lft", "u_e"]:

    if test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication", "region", "rural_urban", "serious_mental_illness", "sex"]:

        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{test}_rate.csv",
            parse_dates=["date"],
        )
        
        if test in ["care_home"]:
            df["care_home"].replace({0: "Not in care home", 1: "In care home"}, inplace=True)
            
        if test in ["dementia"]:
            df["dementia"].replace({0: "No Dementia", 1: "Has Dementia"}, inplace=True)
            
        if test in ["housebound"]:
            df["housebound"].replace({0: "Not Housebound", 1: "Housebound"}, inplace=True)
            
        if test in ["imdQ5"]:
            df["imdQ5"].replace({0: "Missing", 1: "1st Quintile", 2: "2nd Quintile", 3: "3rd Quintile", 4: "4th Quintile", 5: "5th Quintile"}, inplace=True)
            
        if test in ["learning_disability"]:
            df["learning_disability"].replace({0: "No Learning Disability", 1: "Has Learning Disability"}, inplace=True)
            
        if test in ["serious_mental_illness"]:
            df["serious_mental_illness"].replace({0: "No Serious Mental Illness", 1: "Has Serious Mental Illness"}, inplace=True)
            
            
        plot_measures(
            df=df,
            filename=f"/joined/plot_all_sc_overdue_monitoring_by_{test}",
            column_to_plot="value",
            title="",
            y_label="Missed Monitoring Events per Prescription Issue",
            as_bar=False,
            category=f"{test}",
        )
        
        
    if test in ["bp", "fbc", "lft", "u_e"]:

        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_{test}_overdue_rate.csv",
            parse_dates=["date"],
        )

        plot_measures(
            df=df,
            filename=f"/joined/plot_{test}_overdue_rate",
            column_to_plot="value",
            title="",
            y_label="Missed Monitoring Events per Prescription Issue",
            as_bar=False,
            category=f"{test}_overdue_num",
        )
        
        

