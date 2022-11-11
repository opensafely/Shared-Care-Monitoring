import pandas as pd
import numpy as np
import json
from pathlib import Path
from ebmdatalab import charts
from utilities import (
    OUTPUT_DIR,
    ANALYSIS_DIR,
    plot_measures,
    plot_levo,
)

for test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "levothyroxine", "medication", "region", "rural_urban", "serious_mental_illness", "sex", "test_type"]:

    if test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "medication", "region", "rural_urban", "serious_mental_illness", "sex", "test_type"]:

        df = pd.read_csv(
            OUTPUT_DIR / f"rounded/redacted_{test}.csv",
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
            
        if test in ["rural_urban"]:
            df["rural_urban"].replace({-1: "Missing", 1: "1 - Most Rural", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8 - Most Urban"}, inplace=True)
            
            
        plot_measures(
            df=df,
            filename=f"/joined/plot_all_sc_overdue_monitoring_by_{test}",
            column_to_plot="value",
            title="",
            y_label="Patients Overdue Monitoring",
            as_bar=False,
            category=f"{test}",
        )
        
        
    if test in ["levothyroxine"]:

        df = pd.read_csv(
            OUTPUT_DIR / f"rounded/redacted_{test}.csv",
            parse_dates=["date"],
        )

        plot_levo(
            df=df,
            filename=f"/joined/plot_{test}_overdue_rate",
            column_to_plot="value",
            title="",
            y_label="Patients Overdue Monitoring",
            as_bar=False,
        )