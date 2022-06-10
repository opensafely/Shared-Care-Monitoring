from cohortextractor import (
    codelist_from_csv,
)

# Methotrexate Monitoring Rate
methotrexate_codelist = codelist_from_csv(
    "codelists/opensafely-methotrexate-oral.csv",
    system="snomed",
    column="dmd_id",
)

# Azathioprine Monitoring Rate
azathioprine_codelist = codelist_from_csv(
    "codelists/opensafely-azathioprine-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# Leflunomide Monitoring Rate
leflunomide_codelist = codelist_from_csv(
    "codelists/opensafely-leflunomide-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# FBC Monitoring
full_blood_count_codelist = codelist_from_csv(
    "codelists/user-Andrew-fbc-check-represented-by-total-white-cell-count.csv",
    system="snomed",
    column="code",
)

# LFT Monitoring
liver_function_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-lft-check-represented-by-serum-bilirubin-level.csv",
    system="snomed",
    column="code",
)

# U&E Monitoring
urea_electrolyte_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-ue-check-represented-by-serum-creatinine-level.csv",
    system="snomed",
    column="code",
)

# BP Monitoring - used in relation to Leflunomide Monitoring
blood_pressure_test_codelist = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)

# Care Home Resident Status
care_home_codelist = codelist_from_csv(
    "codelists/opensafely-nhs-england-care-homes-residential-status.csv",
    system="snomed",
    column="code",
)