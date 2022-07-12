import pandas as pd
import os
import json
import numpy as np
from utilities import *

subgroups = [                               #not the name of measures, but the name of variables from study definition (column names from input files)
    "all_sc_overdue_monitoring_num",
    "met_overdue_num",
    "lef_overdue_num",
    "aza_overdue_num",
    "fbc_overdue_num",
    "lft_overdue_num",
    "u_e_overdue_num",
    "bp_overdue_num",
]

patient_counts_dict = {}
patient_dict = {}


for file in os.listdir("output"):
    if file.startswith("input"):
        if file.split("_")[1] not in ["ethnicity.csv.gz"]:                           
            file_path = os.path.join("output", file)         #define input file location                              

            df = pd.read_csv(file_path)                      #read input files 

            for measure in subgroups:

                df_subset = df[df[measure] == 1]
                # get unique patients
                patients = list(df_subset["patient_id"])

                if measure not in patient_dict:
                    # create key
                    patient_dict[measure] = patients

                else:
                    patient_dict[measure].extend(patients)


for (key, value) in patient_dict.items():
    # get unique patients
    unique_patients = len(np.unique(patient_dict[key]))

    # add to dictionary as num
    patient_counts_dict[key] = unique_patients

    
df = pd.DataFrame(patient_counts_dict, index=[0])

df.to_csv(
    OUTPUT_DIR / "patient_count.csv", index=False
)