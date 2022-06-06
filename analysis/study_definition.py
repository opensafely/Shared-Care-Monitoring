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

start_date = "2019-09-01"
end_date = "2021-07-01"

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
       (age >=18 AND age <=120) AND 
       (sex = 'M' OR sex = 'F') AND
       (
        (methotrexate_3months) OR
        (leflunomide_3months) OR
        (azathioprine_3months)
       )
       """
    ),
    
    registered=patients.registered_as_of("index_date"),
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "18-29": """ age >= 18 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age <= 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.006,
                    "18-29": 0.142,
                    "30-39": 0.142,
                    "40-49": 0.142,
                    "50-59": 0.142,
                    "60-69": 0.142,
                    "70-79": 0.142,
                    "80+": 0.142,
                }
            },
        },
    ),
    
    practice_population=patients.satisfying(
        """
        age <=120 AND
        registered
        """
    ),
    
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
    ### MEDICATION ISSUES
    methotrexate_3months=patients.with_these_medications(
        codelist=methotrexate_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    leflunomide_3months=patients.with_these_medications(
        codelist=leflunomide_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    azathioprine_3months=patients.with_these_medications(
        codelist=azathioprine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    ### MONITORING PARAMETERS
    full_blood_count=patients.with_these_clinical_events(
        codelist=full_blood_count_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    liver_function_test=patients.with_these_clinical_events(
        codelist=liver_function_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    urea_electroyte_test=patients.with_these_clinical_events(
        codelist=urea_electrolyte_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    #blood_pressure_test=patients.with_these_clinical_events(
    #    codelist=blood_pressure_codelist,
    #    find_last_match_in_period=True,
    #    returning="binary_flag",
    #    between=["index_date - 3 months", "index_date"],
    #),
   
    
    ### NUMERATOR & DENOMINATOR DEFINITIONS
    all_sc_overdue_monitoring_num=patients.satisfying(
        """
        (
            methotrexate_3months OR
            leflunomide_3months OR
            azathioprine_3months
        )
        AND
        (
            NOT full_blood_count OR
            NOT liver_function_test OR
            NOT urea_electroyte_test
        )
        """,
    ),
   
    #first criteria is just the population to maybe don't need it at all?
    
    #    AND
    #    (
    #    IF leflunomide_3months 
    #    NOT blood_pressure_test
   
            
    
    met_overdue_monitoring_num=patients.satisfying(
        """
        methotrexate_3months AND
        (
            NOT full_blood_count OR
            NOT liver_function_test OR
            NOT urea_electroyte_test
        )
        """,
    ),
    
    
    met_overdue_monitoring_den=patients.satisfying(
        """
        methotrexate_3months
        """,
    ),
    
    
    lef_overdue_monitoring_num=patients.satisfying(
        """
        leflunomide_3months AND
        (
            NOT full_blood_count OR
            NOT liver_function_test OR
            NOT urea_electroyte_test OR
            NOT blood_pressure_test
        )
        """,
    ),
    
    
    lef_overdue_monitoring_den=patients.satisfying(
        """
        leflunomide_3months
        """,
    ),
    
    
    aza_overdue_monitoring_num=patients.satisfying(
        """
        azathioprine_3months AND
        (
            NOT full_blood_count OR
            NOT liver_function_test OR
            NOT urea_electroyte_test
        )
        """,
    ),
    
    
    aza_overdue_monitoring_den=patients.satisfying(
        """
        azathioprine_3months
        """,
    ),   
)


### MEASURES
measures = [
    Measure(
        id="all_sc_overdue_monitoring",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="practice",
    ),
    
    Measure(
        id="met_overdue_monitoring",
        numerator="met_overdue_monitoring_num",
        denominator="met_overdue_monitoring_den",
    ),
    
    Measure(
        id="lef_overdue_monitoring",
        numerator="lef_overdue_monitoring_num",
        denominator="lef_overdue_monitoring_den",
    ),
    
    Measure(
        id="aza_overdue_monitoring",
        numerator="aza_overdue_monitoring_num",
        denominator="aza_overdue_monitoring_den",
    ),
    
]
