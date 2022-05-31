# Used in Methotrexate Monitoring Rate
methotrexate_codelist = codelist_from_csv(
    "codelists/opensafely-methotrexate-oral.csv",
    system="snomed",
    column="id",
)

# Used in Azathioprine Monitoring Rate
azathioprine_codelist = codelist_from_csv(
    "codelists/opensafely-azathioprine-dmd.csv",
    system="snomed",
    column="id",
)


# Used in Leflunomide Monitoring Rate
leflunomide_codelist = codelist_from_csv(
    "codelists/opensafely-leflunomide-dmd.csv",
    system="snomed",
    column="id",
)