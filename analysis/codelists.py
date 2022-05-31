from cohortextractor import (
    codelist_from_csv,
)

# Used in Methotrexate Monitoring Rate
methotrexate_codelist = codelist_from_csv(
    "codelists/opensafely-methotrexate-oral.csv",
    system="snomed",
    column="dmd_id",
)

# Used in Azathioprine Monitoring Rate
azathioprine_codelist = codelist_from_csv(
    "codelists/opensafely-azathioprine-dmd.csv",
    system="snomed",
    column="dmd_id",
)


# Used in Leflunomide Monitoring Rate
leflunomide_codelist = codelist_from_csv(
    "codelists/opensafely-leflunomide-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# Used in FBC Monitoring Rate
full_blood_count_codelist = codelist_from_csv(
    "codelists/user-Andrew-fbc-check-represented-by-total-white-cell-count.csv",
    system="snomed",
    column="code",
)

# Used in LFT Monitoring Rate
liver_function_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-lft-check-represented-by-serum-bilirubin-level.csv",
    system="snomed",
    column="code",
)

# Used in U&E Monitoring Rate
urea_electrolyte_test_codelist = codelist_from_csv(
    "codelists/user-Andrew-ue-check-represented-by-serum-creatinine-level.csv",
    system="snomed",
    column="code",
)

