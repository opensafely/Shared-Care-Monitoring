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

start_date = "2019-12-01"
end_date = "2022-08-01"

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
       (imd != -1) AND
       (rural_urban != -1) AND
       (
        (on_methotrexate) OR
        (on_leflunomide) OR
        (on_azathioprine)
       )
       """
    ),
    
    registered=patients.registered_as_of("index_date - 1 day"),
    died=patients.died_from_any_cause(
        on_or_before="index_date - 1 day",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    
    ### DEMOGRAPHICS ----
    
    # GP Practice
    practice=patients.registered_practice_as_of(
        "index_date - 1 day",
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
            "index_date - 1 day",
            return_expectations={
                "rate": "universal",
                "int": {"distribution": "population_ages"},
            },
        ),
    ),
    
    # Region
    region = patients.registered_practice_as_of(
        "index_date - 1 day",
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
    
    # Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
    # Care Home Resident
    care_home=patients.with_these_clinical_events(
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
            on_or_before = "index_date - 1 day",
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
            "index_date - 1 day",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.00,
                    "1": 0.2,
                    "2": 0.2,
                    "3": 0.2,
                    "4": 0.2,
                    "5": 0.2,
                }
            },
        },
    ),

    # Rurality Classification
    rural_urban = patients.address_as_of(
        "index_date - 1 day",
        returning = "rural_urban_classification",
        return_expectations = {
            "rate": "universal",
            "category": {"ratios": {-1: 0.04, 1: 0.12, 2: 0.12, 3: 0.12, 4: 0.12, 5: 0.12, 6: 0.12, 7: 0.12, 8: 0.12}},
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
            on_or_before = "index_date - 1 day",
            returning = "binary_flag",
            return_expectations = {"incidence": 0.05}
        ),
    ),
    
    # Learning Disability
    learning_disability = patients.with_these_clinical_events(
        learning_disability_codes,
        on_or_before = "index_date - 1 day",
        returning = "binary_flag",
        return_expectations = {"incidence": 0.2}
    ),
    
    # Serious Mental Illness
    serious_mental_illness = patients.with_these_clinical_events(
        serious_mental_illness_codes,
        on_or_before = "index_date - 1 day",
        returning = "binary_flag",
        return_expectations = {"incidence": 0.1}
    ),
    
    
    ### MEDICATION ISSUES ----
    
    # Methotrexate within 3m
    methotrexate_3months=patients.with_these_medications(
        codelist=methotrexate_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"]
    ),
    
    # Leflunomide within 3m
    leflunomide_3months=patients.with_these_medications(
        codelist=leflunomide_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"]
    ),
    
    # Azathioprine within 3m
    azathioprine_3months=patients.with_these_medications(
        codelist=azathioprine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"]
    ),
    
    # Methotrexate within 3-6m
    methotrexate_3to6months=patients.with_these_medications(
        codelist=methotrexate_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 6 months", "index_date - 3 months"]
    ),
    
    # Leflunomide within 3-6m
    leflunomide_3to6months=patients.with_these_medications(
        codelist=leflunomide_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 6 months", "index_date - 3 months"]
    ),
    
    # Azathioprine within 3-6m
    azathioprine_3to6months=patients.with_these_medications(
        codelist=azathioprine_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 6 months", "index_date - 3 months"]
    ),
    
    # On Methotrexate
    on_methotrexate=patients.satisfying(
        """
            methotrexate_3months AND
            methotrexate_3to6months AND
            NOT leflunomide_3months AND
            NOT azathioprine_3months
        """,
    ),
    
    # On Leflunomide
    on_leflunomide=patients.satisfying(
        """
            leflunomide_3months AND
            leflunomide_3to6months AND
            NOT methotrexate_3months AND
            NOT azathioprine_3months
        """,
    ),
    
    # On Azathioprine
    on_azathioprine=patients.satisfying(
        """
            azathioprine_3months AND
            azathioprine_3to6months AND
            NOT methotrexate_3months AND
            NOT leflunomide_3months
        """,
    ), 
    

    ### MONITORING PARAMETERS ----
    
    # Full Blood Count
    full_blood_count_3months=patients.with_these_clinical_events(
        codelist=full_blood_count_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"],
    ),
    
    # Liver Function Test
    liver_function_test_3months=patients.with_these_clinical_events(
        codelist=liver_function_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"],
    ),
    
    # Urea & Electrolyte Test
    urea_electrolyte_test_3months=patients.with_these_clinical_events(
        codelist=urea_electrolyte_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"],
    ),
    
    #Blood Pressure Test
    blood_pressure_test_3months=patients.with_these_clinical_events(
        codelist=blood_pressure_test_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date - 1 day"],
    ),
   
    
    ### NUMERATOR DEFINITIONS ----
            
    # On Methotrexate Overdue Any Monitoring
    met_overdue_num=patients.satisfying(
        """
        on_methotrexate AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months
        )
        """,
    ),
    
    # On Leflunomide Overdue Any Monitoring
    lef_overdue_num=patients.satisfying(
        """
        on_leflunomide AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months OR
            NOT blood_pressure_test_3months
        )
        """,
    ),
    
    # On Azathioprine Overdue Any Monitoring
    aza_overdue_num=patients.satisfying(
        """
        on_azathioprine AND
        (
            NOT full_blood_count_3months OR
            NOT liver_function_test_3months OR
            NOT urea_electrolyte_test_3months
        )
        """,
    ),
    
    # All Shared Care Medications Overdue Any Monitoring
    all_sc_overdue_monitoring_num=patients.satisfying(
        """
        met_overdue_num OR
        aza_overdue_num OR
        lef_overdue_num
        """,
    ),
    
    # Categorise for Shared Care Medication Issued
    medication = patients.categorised_as(
        {
            "no_meds": "DEFAULT",
            "Leflunomide": "on_leflunomide",
            "Methotrexate": "on_methotrexate",
            "Azathioprine": "on_azathioprine",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "no_meds": 0,
                    "Leflunomide": 0.33,
                    "Methotrexate": 0.34,
                    "Azathioprine": 0.33,
                }
            },
        },
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
        on_leflunomide AND
        NOT blood_pressure_test_3months
        """,
    ),
)
    

### MEASURES ----
measures = [

    #OVERALL
    Measure(
        id="all_sc_overdue_monitoring_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="population",
    ), 

    
    #GROUPED BY MEDICATION
    Measure(
        id="all_sc_overdue_monitoring_by_medication_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="medication",
    ),  
         
    
    #MONITORING TEST BREAKDOWN
    Measure(
        id="fbc_overdue_rate",
        numerator="fbc_overdue_num",
        denominator="population",
        group_by="population",
    ),
    
    Measure(
        id="lft_overdue_rate",
        numerator="lft_overdue_num",
        denominator="population",
        group_by="population",
    ),
    
    Measure(
        id="u_e_overdue_rate",
        numerator="u_e_overdue_num",
        denominator="population",
        group_by="population",
    ),
    
    Measure(
        id="bp_overdue_rate",
        numerator="bp_overdue_num",
        denominator="on_leflunomide",
        group_by="population",
    ),
    

    #DEMOGRAPHIC GROUP BREAKDOWN
    Measure(
        id="all_sc_overdue_monitoring_by_age_band_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="age_band",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_sex_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="sex",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_region_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="region",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_practice_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="practice",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_ethnicity_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="ethnicity",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_imdQ5_rate", 
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="imdQ5",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_rural_urban_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="rural_urban",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_care_home_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="care_home",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_housebound_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="housebound",
    ),
    
    #CLINICAL GROUP BREAKDOWN
    Measure(
        id="all_sc_overdue_monitoring_by_dementia_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="dementia",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_learning_disability_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="learning_disability",
    ),
    
    Measure(
        id="all_sc_overdue_monitoring_by_serious_mental_illness_rate",
        numerator="all_sc_overdue_monitoring_num",
        denominator="population",
        group_by="serious_mental_illness",
    ),  
]