from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
    Measure
)

from codelists import *

start_date = "2020-02-01"
end_date = "2020-06-01"

study = StudyDefinition(
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    
    population=patients.satisfying(
        """
       registered AND
       NOT died AND
       (age != "missing") AND
       (age >=  18 AND age <= 120) AND
       (sex = 'M' OR sex = 'F') AND
       (
        (on_levothyroxine)
       )
       """
    ),
    
    registered=patients.registered_as_of("index_date"),
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        }
    ),
    
    # Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
    
    ### MEDICATION ISSUES ----

    # Levothyroxine within 3m
    levothyroxine_3months=patients.with_these_medications(
        codelist=levothyroxine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    # Levothyroxine within 3-6m
    levothyroxine_3to6months=patients.with_these_medications(
        codelist=levothyroxine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 6 months", "index_date - 3 months"]
    ),
    
    # On Levothyroxine
    on_levothyroxine=patients.satisfying(
        """
            levothyroxine_3months AND
            levothyroxine_3to6months
        """,
    ),
    

    ### MONITORING PARAMETERS ----
    
    # Thyroid Function Test
    thyroid_function_test_12months=patients.with_these_clinical_events(
        codelist=thyroid_stimulating_hormone_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 12 months", "index_date"],
    ),

    
    ### NUMERATOR DEFINITION ----
            
    # On Levothyroxine and Overdue Thyroid Function Test
    levothyroxine_overdue_num=patients.satisfying(
        """
        on_levothyroxine AND
        (
            NOT thyroid_function_test_12months
        )
        """,
    ),
)
    

### MEASURE ----
measures = [

    Measure(
        id="levothyroxine_overdue_rate",
        numerator="levothyroxine_overdue_num",
        denominator="population",
        group_by="population",
    ),
    
]   