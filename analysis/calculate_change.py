import pandas as pd
import numpy as np
import json
from utilities import *


measures = ["age_band", "care_home", "dementia", "ethnicity", "housebound", "imdQ5", "learning_disability", "region", "rural_urban", "serious_mental_illness", "sex"]

#data_dict = {}

for measure in measures:
     
    df = pd.read_csv(
        OUTPUT_DIR / f"joined/measure_all_sc_overdue_monitoring_by_{measure}_rate.csv",        #load a df
        parse_dates=["date"],
     )
    
    if measure in ["care_home", "dementia", "housebound", "learning_disability", "serious_mental_illness"]:

        #Identify value ranges for binary subgroups in Feb20
        feb20_not_subgroup = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==0)),"value"]  #All patients NOT in the subgroup Feb20
        feb20_in_subgroup = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==1)),"value"]  #All patients IN the subgroup Feb20
        
        #Identify value ranges for binary subgroups in May20
        may20_not_subgroup = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==0)),"value"]  #All patients NOT in the subgroup May20
        may20_in_subgroup = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==1)),"value"]  #All patients IN the subgroup May20

        #Calculate change between rates at relevant dates NOT IN / IN subgroup
        feb20tomay20_change_not_subgroup = may20_not_subgroup.sum() - feb20_not_subgroup.sum()
        feb20tomay20_change_in_subgroup = may20_in_subgroup.sum() - feb20_in_subgroup.sum()

        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series([0, 1]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_not_subgroup, feb20tomay20_change_in_subgroup])})

        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )
  
    if measure in ["imdQ5"]:

        #Identify value ranges for various IMD Quintiles in Feb20
        feb20_first_quintile = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==1)),"value"]
        feb20_second_quintile = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==2)),"value"]
        feb20_third_quintile = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==3)),"value"]
        feb20_fourth_quintile = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==4)),"value"]
        feb20_fifth_quintile = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==5)),"value"]
        
        #Identify value ranges for various IMD Quintiles in May20
        may20_first_quintile = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==1)),"value"]
        may20_second_quintile = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==2)),"value"]
        may20_third_quintile = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==3)),"value"]
        may20_fourth_quintile = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==4)),"value"]
        may20_fifth_quintile = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==5)),"value"]

        #Calculate change between rates at relevant dates for each IMD Quintile
        feb20tomay20_change_first_quintile = may20_first_quintile.sum() - feb20_first_quintile.sum()
        feb20tomay20_change_second_quintile = may20_second_quintile.sum() - feb20_second_quintile.sum()
        feb20tomay20_change_third_quintile = may20_third_quintile.sum() - feb20_third_quintile.sum()
        feb20tomay20_change_fourth_quintile = may20_fourth_quintile.sum() - feb20_fourth_quintile.sum()
        feb20tomay20_change_fifth_quintile = may20_fifth_quintile.sum() - feb20_fifth_quintile.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["First Quintile", "Second Quintile", "Third Quintile", "Fourth Quintile", "Fifth Quintile"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_first_quintile, feb20tomay20_change_second_quintile, feb20tomay20_change_third_quintile, feb20tomay20_change_fourth_quintile, feb20tomay20_change_fifth_quintile])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )

    if measure in ["age_band"]:
            
        #Identify value ranges for various age bands in Feb20        
        feb20_18to29 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="18-29")),"value"]   
        feb20_30to39 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="30-39")),"value"]
        feb20_40to49 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="40-49")),"value"]
        feb20_50to59 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="50-59")),"value"]
        feb20_60to69 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="60-69")),"value"]
        feb20_70to79 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="70-79")),"value"]
        feb20_80plus = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="80+")),"value"]

        #Identify value ranges for various age bands in May20
        may20_18to29 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="18-29")),"value"]
        may20_30to39 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="30-39")),"value"]
        may20_40to49 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="40-49")),"value"]
        may20_50to59 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="50-59")),"value"]
        may20_60to69 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="60-69")),"value"]
        may20_70to79 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="70-79")),"value"]
        may20_80plus = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="80+")),"value"]

        #Calculate change between rates at relevant dates for each age band
        feb20tomay20_change_18to29 = may20_18to29.sum() - feb20_18to29.sum()
        feb20tomay20_change_30to39 = may20_30to39.sum() - feb20_30to39.sum()
        feb20tomay20_change_40to49 = may20_40to49.sum() - feb20_40to49.sum()
        feb20tomay20_change_50to59 = may20_50to59.sum() - feb20_50to59.sum()
        feb20tomay20_change_60to69 = may20_60to69.sum() - feb20_60to69.sum()
        feb20tomay20_change_70to79 = may20_70to79.sum() - feb20_70to79.sum()
        feb20tomay20_change_80plus = may20_80plus.sum() - feb20_80plus.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_18to29, feb20tomay20_change_30to39, feb20tomay20_change_40to49, feb20tomay20_change_50to59, feb20tomay20_change_60to69, feb20tomay20_change_70to79, feb20tomay20_change_80plus])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )
        
        
    if measure in ["ethnicity"]:
            
    #may need to change pending confirmation of labels for 6 categories
        
        #Identify value ranges for various ethnicities in Feb20        
        feb20_black = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="Black")),"value"]   
        feb20_mixed = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="Mixed")),"value"]
        feb20_other = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="Other")),"value"]
        feb20_south_asian = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="South Asian")),"value"]
        feb20_white = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="White")),"value"]

        #Identify value ranges for various ethnicities in May20
        may20_black = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="Black")),"value"]
        may20_mixed = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="Mixed")),"value"]
        may20_other = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="Other")),"value"]
        may20_south_asian = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="South Asian")),"value"]
        may20_white = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="White")),"value"]

        #Calculate change between rates at relevant dates for each ethnicity
        feb20tomay20_change_black = may20_black.sum() - feb20_black.sum()
        feb20tomay20_change_mixed = may20_mixed.sum() - feb20_mixed.sum()
        feb20tomay20_change_other = may20_other.sum() - feb20_other.sum()
        feb20tomay20_change_south_asian = may20_south_asian.sum() - feb20_south_asian.sum()
        feb20tomay20_change_white = may20_white.sum() - feb20_white.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["Black", "Mixed", "Other", "South Asian", "White"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_black, feb20tomay20_change_mixed, feb20tomay20_change_other, feb20tomay20_change_south_asian, feb20tomay20_change_white])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )
        
        
    if measure in ["region"]:
            
        #Identify value ranges for various regions in Feb20        
        feb20_east = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="East")),"value"]   
        feb20_east_midlands = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="East Midlands")),"value"]
        feb20_london = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="London")),"value"]
        feb20_north_east = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="North East")),"value"]
        feb20_north_west = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="North West")),"value"]
        feb20_south_east = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="South East")),"value"]
        feb20_south_west = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="South West")),"value"]
        feb20_west_midlands = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="West Midlands")),"value"]
        feb20_yorkshire = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="Yorkshire and The Humber")),"value"]

        #Identify value ranges for various regions in May20
        may20_east = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="East")),"value"]   
        may20_east_midlands = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="East Midlands")),"value"]
        may20_london = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="London")),"value"]
        may20_north_east = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="North East")),"value"]
        may20_north_west = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="North West")),"value"]
        may20_south_east = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="South East")),"value"]
        may20_south_west = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="South West")),"value"]
        may20_west_midlands = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="West Midlands")),"value"]
        may20_yorkshire = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="Yorkshire and The Humber")),"value"]

        #Calculate change between rates at relevant dates for each region
        feb20tomay20_change_east = may20_east.sum() - feb20_east.sum()
        feb20tomay20_change_east_midlands = may20_east_midlands.sum() - feb20_east_midlands.sum()
        feb20tomay20_change_london = may20_london.sum() - feb20_london.sum()
        feb20tomay20_change_north_east = may20_north_east.sum() - feb20_north_east.sum()
        feb20tomay20_change_north_west = may20_north_west.sum() - feb20_north_west.sum()
        feb20tomay20_change_south_east = may20_south_east.sum() - feb20_south_east.sum()
        feb20tomay20_change_south_west = may20_south_west.sum() - feb20_south_west.sum()
        feb20tomay20_change_west_midlands = may20_west_midlands.sum() - feb20_west_midlands.sum()
        feb20tomay20_change_yorkshire = may20_yorkshire.sum() - feb20_yorkshire.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["East", "East Midlands", "London", "North East", "North West", "South East", "South West", "West Midlands", "Yorkshire and The Humber"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_east, feb20tomay20_change_east_midlands, feb20tomay20_change_london, feb20tomay20_change_north_east, feb20tomay20_change_north_west, feb20tomay20_change_south_east, feb20tomay20_change_south_west, feb20tomay20_change_west_midlands, feb20tomay20_change_yorkshire])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )
        
        
    if measure in ["rural_urban"]:
            
        #Identify value ranges for various rurality scores in Feb20        
        feb20_1 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==1)),"value"]   
        feb20_2 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==2)),"value"]
        feb20_3 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==3)),"value"]
        feb20_4 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==4)),"value"]
        feb20_5 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==5)),"value"]
        feb20_6 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==6)),"value"]
        feb20_7 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==7)),"value"]
        feb20_8 = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]==8)),"value"]

        #Identify value ranges for various rurality scores in May20
        may20_1 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==1)),"value"]   
        may20_2 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==2)),"value"]
        may20_3 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==3)),"value"]
        may20_4 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==4)),"value"]
        may20_5 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==5)),"value"]
        may20_6 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==6)),"value"]
        may20_7 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==7)),"value"]
        may20_8 = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]==8)),"value"]

        #Calculate change between rates at relevant dates for each rurality score
        feb20tomay20_change_1 = may20_1.sum() - feb20_1.sum()
        feb20tomay20_change_2 = may20_2.sum() - feb20_2.sum()
        feb20tomay20_change_3 = may20_3.sum() - feb20_3.sum()
        feb20tomay20_change_4 = may20_4.sum() - feb20_4.sum()
        feb20tomay20_change_5 = may20_5.sum() - feb20_5.sum()
        feb20tomay20_change_6 = may20_6.sum() - feb20_6.sum()
        feb20tomay20_change_7 = may20_7.sum() - feb20_7.sum()
        feb20tomay20_change_8 = may20_8.sum() - feb20_8.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["1", "2", "3", "4", "5", "6", "7", "8"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_1, feb20tomay20_change_2, feb20tomay20_change_3, feb20tomay20_change_4, feb20tomay20_change_5, feb20tomay20_change_6, feb20tomay20_change_7, feb20tomay20_change_8])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )
        
        
    if measure in ["sex"]:
            
        #Identify value ranges for both sexes in Feb20        
        feb20_male = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="M")),"value"]   
        feb20_female = df.loc[((df["date"]=="2020-03-01") & (df[f"{measure}"]=="F")),"value"]

        #Identify value ranges for various rurality scores in May20
        may20_male = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="M")),"value"]   
        may20_female = df.loc[((df["date"]=="2020-06-01") & (df[f"{measure}"]=="F")),"value"]

        #Calculate change between rates at relevant dates for each rurality score
        feb20tomay20_change_male = may20_male.sum() - feb20_male.sum()
        feb20tomay20_change_female = may20_female.sum() - feb20_female.sum()
        
        #Create new dataframe which contains calculated values
        df = pd.DataFrame({f"{measure}": pd.Series(["Male", "Female"]), "Rate Change Feb20-May20": pd.Series([feb20tomay20_change_male, feb20tomay20_change_female])})
        
        #Output new dataframe with calculated values as a new table
        df.to_csv(
            OUTPUT_DIR / f"joined/changes_{measure}.csv", index=False
        )

        
"""
        data_dict[measure] = []
        
        data_dict[measure].append(feb20tomay20_change_in_subgroup)
        
        df = pd.DataFrame(data_dict, index=[0])
        
        df.to_csv(
                OUTPUT_DIR / "joined/summary_changes.csv", index=False
        )
"""
