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

for test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex", "aza", "met", "lef", "bp", "fbc", "lft", "u_e"]:

    if test in ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex"]:

        df = pd.read_csv(
            OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{test}_rate.csv",
            parse_dates=["date"],
        )

        plot_measures(
            df=df,
            filename=f"/joined/plot_all_sc_overdue_monitoring_by_{test}",
            column_to_plot="value",
            title="",
            y_label="Missed Monitoring Events per Prescription Issue",
            as_bar=False,
            category=f"{test}",
        )
        
    if test in ["aza", "met", "lef", "bp", "fbc", "lft", "u_e"]:

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
        