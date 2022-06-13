from cohortextractor import (
    codelist_from_csv,
)

## MEDICATIONS ----

# Azathioprine
azathioprine_codelist = codelist_from_csv(
    "codelists/opensafely-azathioprine-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# Leflunomide
leflunomide_codelist = codelist_from_csv(
    "codelists/opensafely-leflunomide-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# Methotrexate
methotrexate_codelist = codelist_from_csv(
    "codelists/opensafely-methotrexate-oral.csv",
    system="snomed",
    column="dmd_id",
)


## MONITORING PARAMETERS ----

# FBC
full_blood_count_codelist = codelist_from_csv(
    "codelists/user-Andrew-fbc-check-represented-by-total-white-cell-count.csv",
    system="snomed",
    column="code",
)

# LFT
liver_function_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-lft-check-represented-by-serum-bilirubin-level.csv",
    system="snomed",
    column="code",
)

# U&E
urea_electrolyte_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-ue-check-represented-by-serum-creatinine-level.csv",
    system="snomed",
    column="code",
)

# BP
blood_pressure_test_codelist = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)


## COVARIATES ----

# Care Home Resident Status
care_home_codelist = codelist_from_csv(
    "codelists/opensafely-nhs-england-care-homes-residential-status.csv",
    system="snomed",
    column="code",
)

# Dementia
dementia_nhsd_snomed_codes = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dem_cod.csv", 
  system = "snomed", 
  column = "code",
)

# Ethnicity - 6 Grouping
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)

# Housebound
housebound_opensafely_snomed_codes = codelist_from_csv(
    "codelists/opensafely-housebound.csv", 
    system = "snomed", 
    column = "code"
)

no_longer_housebound_opensafely_snomed_codes = codelist_from_csv(
    "codelists/opensafely-no-longer-housebound.csv", 
    system = "snomed", 
    column = "code"
)

# Learning disabilities
wider_ld_primis_snomed_codes = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-learndis.csv", 
    system = "snomed", 
    column = "code"
)

# Serious mental illness
serious_mental_illness_codes = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-mh_cod.csv",
  system = "snomed",
  column = "code",
)

