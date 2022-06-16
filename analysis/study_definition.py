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
       (age_band != "missing") AND 
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
    
    ### DEMOGRAPHICS ----
    
    # GP Practice
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),

    # Age Band
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
    
        age=patients.age_as_of(
            "index_date",
            return_expectations={
                "rate": "universal",
                "int": {"distribution": "population_ages"},
            },
        ),
    ),
    
    # Region
    region = patients.registered_practice_as_of(
        "index_date",
        returning = "nuts1_region_name",
        return_expectations = {
          "rate": "universal",
          "category": {
            "ratios": {
              "North East": 0.1,
              "North West": 0.1,
              "Yorkshire and The Humber": 0.1,
              "East Midlands": 0.1,
              "West Midlands": 0.1,
              "East": 0.1,
              "London": 0.2,
              "South East": 0.1,
              "South West": 0.1,
            },
          },
        },
    ),
    
    # Ethnicity
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
    
    # Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
    # Care Home Resident
    care_home_resident=patients.with_these_clinical_events(
        codelist=care_home_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
    ),
    
    # Housebound
    housebound = patients.satisfying(
    """housebound_date
                AND NOT no_longer_housebound
                AND NOT moved_into_care_home""",
    return_expectations={
      "incidence": 0.01,
    },
    
        housebound_date = patients.with_these_clinical_events( 
            codelist = housebound_opensafely_snomed_codes, 
            on_or_before = "index_date",
            find_last_match_in_period = True,
            returning = "date",
            date_format = "YYYY-MM-DD",
        ),   

        no_longer_housebound = patients.with_these_clinical_events( 
            codelist = no_longer_housebound_opensafely_snomed_codes, 
            between=["housebound_date", "index_date - 3 months"]
        ),

        moved_into_care_home = patients.with_these_clinical_events(
            codelist = care_home_codelist,
            between=["housebound_date", "index_date - 3 months"]
        ),
    ),
    
   # Index of Multiple Deprivation Quintile
    imdQ5=patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": "imd >= 0 AND imd < 32800*1/5",
            "2": "imd >= 32800*1/5 AND imd < 32800*2/5",
            "3": "imd >= 32800*2/5 AND imd < 32800*3/5",
            "4": "imd >= 32800*3/5 AND imd < 32800*4/5",
            "5": "imd >= 32800*4/5 AND imd <= 32800",
        },
        imd=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.05,
                    "1": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5": 0.19,
                }
            },
        },
    ),

    # Rurality Classification
    rural_urban = patients.address_as_of(
        "index_date",
        returning = "rural_urban_classification",
        return_expectations = {
            "rate": "universal",
            "category": {"ratios": {1: 0.125, 2: 0.125, 3: 0.125, 4: 0.125, 5: 0.125, 6: 0.125, 7: 0.125, 8: 0.125}},
            "incidence": 1,
        },
    ),
    
    
    ### CLINICAL COVARIATES ----
    
    # Dementia
    dementia = patients.satisfying(
        """
        dementia_all
        AND
        age > 39
        """, 
    return_expectations = {
      "incidence": 0.01,
    },
        
        dementia_all = patients.with_these_clinical_events(
            dementia_nhsd_snomed_codes,
            on_or_before = "index_date",
            returning = "binary_flag",
            return_expectations = {"incidence": 0.05}
        ),
    ),
    
    # Learning Disability
    learning_disability = patients.with_these_clinical_events(
        learning_disability_codes,
        on_or_before = "index_date",
        returning = "binary_flag",
        return_expectations = {"incidence": 0.2}
    ),
    
    # Serious Mental Illness
    serious_mental_illness = patients.with_these_clinical_events(
        serious_mental_illness_codes,
        on_or_before = "index_date",
        returning = "binary_flag",
        return_expectations = {"incidence": 0.1}
    ),
    
    
    ### MEDICATION ISSUES ----
    
    # Methotrexate
    methotrexate_3months=patients.with_these_medications(
        codelist=methotrexate_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    # Leflunomide
    leflunomide_3months=patients.with_these_medications(
        codelist=leflunomide_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    # Azathioprine
    azathioprine_3months=patients.with_these_medications(
        codelist=azathioprine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"]
    ),
    
    
    ### MONITORING PARAMETERS ----
    
    # Full Blood Count
    full_blood_count_3months=patients.with_these_clinical_events(
        codelist=full_blood_count_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    # Liver Function Test
    liver_function_test_3months=patients.with_these_clinical_events(
        codelist=liver_function_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    # Urea & Electrolyte Test
    urea_electrolyte_test_3months=patients.with_these_clinical_events(
        codelist=urea_electrolyte_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
    
    #Blood Pressure Test
    blood_pressure_test_3months=patients.with_these_clinical_events(
        codelist=blood_pressure_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),
   
    
    ### NUMERATOR DEFINITIONS ----
            
    # On Methotrexate Overdue Any Monitoring
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
    
    # On Leflunomide Overdue Any Monitoring
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
    
    # On Azathioprine Overdue Any Monitoring
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
    
    # All Shared Care Medicines Overdue Any Monitoring
    all_sc_overdue_monitoring_num=patients.satisfying(
        """
        met_overdue_monitoring_num OR
        aza_overdue_monitoring_num OR
        lef_overdue_monitoring_num
        """,
    ),
    
    # No Full Blood Count within 3 months
    fbc_overdue_num=patients.satisfying(
        """
        (NOT full_blood_count_3months)
        """,
    ),
    
    # No Liver Function Test within 3 months
    lft_overdue_num=patients.satisfying(
        """
        (NOT liver_function_test_3months)
        """,
    ),
    
    # No Urea & Electrolyte Test within 3 months
    u_e_overdue_num=patients.satisfying(
        """
        (NOT urea_electrolyte_test_3months)
        """,
    ),
    
    # No Blood Pressure Test within 3 months - only relevant to Leflunomide
    bp_overdue_num=patients.satisfying(
        """
        leflunomide_3months AND
        NOT blood_pressure_test_3months
        """,
    ),
)


### MEASURES ----
measures = [
   
    #OVERALL
    Measure(
        id="all_sc_overdue_monitoring_by_practice",
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
    
    #MONITORING PARAMETER BREAKDOWN
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
    
    Measure(
        id="bp_overdue",
        numerator="bp_overdue_num",
        denominator="leflunomide_3months",
    ),
    
]
