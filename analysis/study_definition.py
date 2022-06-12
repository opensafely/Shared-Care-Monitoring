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
    
    
     ethnicity = patients.categorised_as(
            {"Missing": "DEFAULT",
            "White": "eth='1' OR (NOT eth AND ethnicity_sus='1')", 
            "Mixed": "eth='2' OR (NOT eth AND ethnicity_sus='2')", 
            "South Asian": "eth='3' OR (NOT eth AND ethnicity_sus='3')", 
            "Black": "eth='4' OR (NOT eth AND ethnicity_sus='4')",  
            "Other": "eth='5' OR (NOT eth AND ethnicity_sus='5')",
            }, 
            return_expectations={
            "category": {"ratios": {"White": 0.2, "Mixed": 0.2, "South Asian": 0.2, "Black": 0.2, "Other": 0.2}},
            "incidence": 0.4,
            },

            ethnicity_sus = patients.with_ethnicity_from_sus(
                returning="group_6",  
                use_most_frequent_code=True,
                return_expectations={
                    "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                    "incidence": 0.4,
                    },
            ),

            eth=patients.with_these_clinical_events(
                ethnicity_codes,
                returning="category",
                find_last_match_in_period=True,
                on_or_before="index_date",
                return_expectations={
                    "category": {"ratios": {"1": 0.4, "2": 0.4, "3": 0.2, "4":0.2,"5": 0.2}},
                    "incidence": 0.75,
                },
            ),
    ),
    
    
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
         
    care_home_resident=patients.with_these_clinical_events(
        codelist=care_home_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
    ),
    
    
    practice_population=patients.satisfying(
        """
        age <=120 AND
        registered
        """
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
    full_blood_count_3months=patients.with_these_clinical_events(
        codelist=full_blood_count_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    liver_function_test_3months=patients.with_these_clinical_events(
        codelist=liver_function_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    urea_electrolyte_test_3months=patients.with_these_clinical_events(
        codelist=urea_electrolyte_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    blood_pressure_test_3months=patients.with_these_clinical_events(
        codelist=blood_pressure_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
   
    
    ### NUMERATOR & DENOMINATOR DEFINITIONS
    all_sc_overdue_monitoring_num=patients.satisfying(
        """
        (
            (
                methotrexate_3months OR
                azathioprine_3months
            )
            AND
            (
                NOT full_blood_count_3months OR
                NOT liver_function_test_3months OR
                NOT urea_electrolyte_test_3months
            )
        )
        OR
        (
            (
                leflunomide_3months
            )
            AND
            (
                NOT full_blood_count_3months OR
                NOT liver_function_test_3months OR
                NOT urea_electrolyte_test_3months OR
                NOT blood_pressure_test_3months
            )
        )
        """,
    ),
            
    
    met_overdue_monitoring_num=patients.satisfying(
        """
        methotrexate_3months AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months
        )
        """,
    ),
    
    
    lef_overdue_monitoring_num=patients.satisfying(
        """
        leflunomide_3months AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months OR
            NOT blood_pressure_test_3months
        )
        """,
    ),
    
    
    aza_overdue_monitoring_num=patients.satisfying(
        """
        azathioprine_3months AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months
        )
        """,
    ),
    
    
    fbc_overdue_num=patients.satisfying(
        """
        (NOT full_blood_count_3months)
        """,
    ),
    
    lft_overdue_num=patients.satisfying(
        """
        (NOT liver_function_test_3months)
        """,
    ),
    
    u_e_overdue_num=patients.satisfying(
        """
        (NOT urea_electrolyte_test_3months)
        """,
    ),
)


### MEASURES
measures = [
   
    #OVERALL
    Measure(
        id="all_sc_overdue_monitoring",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="practice",
    ),
    
    #DRUG BREAKDOWN
    Measure(
        id="met_overdue_monitoring",
        numerator="met_overdue_monitoring_num",
        denominator="methotrexate_3months",
    ),
    
    Measure(
        id="lef_overdue_monitoring",
        numerator="lef_overdue_monitoring_num",
        denominator="leflunomide_3months",
    ),
    
    Measure(
        id="aza_overdue_monitoring",
        numerator="aza_overdue_monitoring_num",
        denominator="azathioprine_3months",
    ),
    
    #TEST BREAKDOWN
    Measure(
        id="fbc_overdue",
        numerator="fbc_overdue_num",
        denominator="population",
    ),
    
    Measure(
        id="lft_overdue",
        numerator="lft_overdue_num",
        denominator="population",
    ),
    
    Measure(
        id="u_e_overdue",
        numerator="u_e_overdue_num",
        denominator="population",
    ),
    
]
