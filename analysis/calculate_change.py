import pandas as pd
import numpy as np
import json
from utilities import *


measures = ["age_band", "care_home", "dementia", "housebound", "imdQ5", "learning_disability", "serious_mental_illness"]

data_dict = {}

for measure in measures:
     
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",        #load a df
        parse_dates=["date"],
     )
    
    if measure in ["care_home", "dementia", "housebound", "learning_disability", "serious_mental_illness"]:

        #Identify value ranges for binary subgroups in Feb20
        feb20_not_subgroup = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]==0),"value"]  #All patients NOT in the subgroup Feb20
        feb20_in_subgroup = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]==1),"value"]  #All patients IN the subgroup Feb20
        
        #Identify value ranges for binary subgroups in May20
        may20_not_subgroup = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]==0),"value"]  #All patients NOT in the subgroup May20
        may20_in_subgroup = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]==1),"value"]  #All patients IN the subgroup May20

        #Calculate change between rates at relevant dates NOT IN / IN subgroup
        feb20tomay20_change_not_subgroup = may20_not_subgroup.sum() - feb20_not_subgroup.sum()
        feb20tomay20_change_in_subgroup = may20_in_subgroup.sum() - feb20_in_subgroup.sum()

        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series([0, 1]), "change_in_rate Feb20-May20": pd.Series([feb20tomay20_change_not_subgroup, feb20tomay20_change_in_subgroup])})

        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/{measure}_changes.csv", index=False
        )
  
    if measure in ["imdQ5"]:

        #Identify value ranges for various IMD Quintiles in Feb20
        feb20_first_quintile = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]==1),"value"]
        feb20_second_quintile = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]==2),"value"]
        
        #Identify value ranges for various IMD Quintiles in May20
        may20_first_quintile = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]==1),"value"]
        may20_second_quintile = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]==2),"value"]

        #Calculate change between rates at relevant dates for each IMD Quintile
        feb20tomay20_change_first_quintile = may20_first_quintile.sum() - feb20_first_quintile.sum()
        feb20tomay20_change_second_quintile = may20_second_quintile.sum() - feb20_second_quintile.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["First Quintile", "Second Quintile"]), "change_in_rate Feb20-May20": pd.Series([feb20tomay20_change_first_quintile, feb20tomay20_change_second_quintile])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/{measure}_changes.csv", index=False
        )

    if measure in ["age_band"]:

        #Identify value ranges for various age bands in Feb20
        feb20_18to29 = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]=="18-29"),"value"]
        feb20_30to39 = df.loc[((df["date"]=="2020-03-01") & df[f"{measure}"]=="30-39"),"value"]

        #Identify value ranges for various age bands in May20
        may20_18to29 = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]=="18-29"),"value"]
        may20_30to39 = df.loc[((df["date"]=="2020-06-01") & df[f"{measure}"]=="30-39"),"value"]

        #Calculate change between rates at relevant dates for each age band
        feb20tomay20_change_18to29 = may20_18to29.sum() - feb20_18to29.sum()
        feb20tomay20_change_30to39 = may20_30to39.sum() - feb20_30to39.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["18-29", "30-39"]), "change_in_rate Feb20-May20": pd.Series([feb20tomay20_change_18to29, feb20tomay20_change_30to39])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/{measure}_changes.csv", index=False
        )

        
"""
        data_dict[measure] = []
        
        data_dict[measure].append(feb20tomay20_change_in_subgroup)
        
        df = pd.DataFrame(data_dict, index=[0])
        
        df.to_csv(
                OUTPUT_DIR / "joined/summary_changes.csv", index=False
        )
"""


