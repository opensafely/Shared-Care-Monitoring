######################################
# Import measures data
######################################

# Preliminaries ----
## Import libraries ----
library('tidyverse')
library('lubridate')
library('here')

## define input/output directories ----

# where the measures files are stored
measures_dir <- here("output", "joined")

# where to output the results
fs::dir_create(here("output", "analysis"))
analysis_dir <- here("output", "analysis")

# Import measures ----
# all measure csv files
measures_path_all <- fs::dir_ls(path=measures_dir, glob="*.csv", type="file")

# only summary files (exclude files with date suffix) ##this line may not be needed because all the date-specific files are saved elwhere or are csv.gz (not csv) files. But it does no harm
measures_path_summary <- measures_path_all[!str_detect(measures_path_all, "\\_\\d+\\-\\d+\\-\\d+\\.csv$")]

# name of measure
measure_name <-
  measures_path_summary %>%
  fs::path_file() %>%
  fs::path_ext_remove()

# import measures data from csv and put each dataset in a list
data_measures <-
  map(
    set_names(measures_path_summary, measure_name),
    function(path){

      measure_name <-
        path %>%
        fs::path_file() %>%
        fs::path_ext_remove()

      dat <- read_csv(path)
      names(dat)[names(dat)==measure_name] <- "events"
      dat$measure_name <- measure_name

      dat
    }
  )

## define time periods dates:
index_baseline <- date("2020-03-01")
index_impact <- date("2020-06-01")

### T - TEST FOR POPULATION
df_ttest_results_population <- data_measures$measure_all_sc_overdue_monitoring_rate %>%
  mutate(
    # assign months to analysis periods
    period = case_when(
      date == index_baseline ~ "baseline",
      date == index_impact ~ "impact",
      TRUE ~ NA_character_
    ),
    numerator = all_sc_overdue_monitoring_num
  ) %>%
  # remove if date is not in comparison period
  filter(!is.na(period)) %>%
  # aggregate data within periods
  group_by(measure_name, period) %>%
  summarise(
    population = sum(population),
    numerator  = sum(numerator),
    value = numerator/population
  ) %>%
  pivot_wider(
    id_cols = c("measure_name"),
    names_from = period,
    values_from = c("population", "numerator", "value")
  ) %>%
  mutate(
    difference = value_impact - value_baseline,
    std.error_baseline = sqrt( (value_baseline*(1-value_baseline))/population_baseline),
    std.error_impact = sqrt( (value_impact*(1-value_impact))/population_impact),
    std.error = sqrt((std.error_baseline^2) + (std.error_impact^2)),
    test.stat = difference/std.error,

    p.value = pchisq(test.stat^2, df=1, lower.tail=FALSE),

    difference.ll = difference + qnorm(0.025)*std.error,
    difference.ul = difference + qnorm(0.975)*std.error) %>%
    ungroup()

# Write results
df_ttest_results_population %>%
  mutate(measure_name = "population") %>%
  write_csv(here("output/analysis/measures_population_ttest.csv"))

# Prepare dataset with subgroups for looping
# Create vector with measure names (only include data that we need for ttests)
measures_ttest <- c("measure_all_sc_overdue_monitoring_by_age_band_rate",
                    "measure_all_sc_overdue_monitoring_by_care_home_rate",
                    "measure_all_sc_overdue_monitoring_by_dementia_rate",
                    "measure_all_sc_overdue_monitoring_by_ethnicity_rate",
                    "measure_all_sc_overdue_monitoring_by_housebound_rate",
                    "measure_all_sc_overdue_monitoring_by_imdQ5_rate",
                    "measure_all_sc_overdue_monitoring_by_learning_disability_rate",
                    "measure_all_sc_overdue_monitoring_by_medication_rate",
                    "measure_all_sc_overdue_monitoring_by_region_rate",
                    "measure_all_sc_overdue_monitoring_by_rural_urban_rate",
                    "measure_all_sc_overdue_monitoring_by_serious_mental_illness_rate",
                    "measure_all_sc_overdue_monitoring_by_sex_rate")

# Create empty list for dataframes (we will use this in the loop)
data_ttest <- list()

# Write for loop that takes only the measures we defined above
for (measure_name in measures_ttest) {
  print(measure_name)
  data_ttest[[measure_name]] <- data_measures[[measure_name]]
}

# Check that the names of the new list only includes the measures we want
names(data_ttest)

# Rename all measure variables to "measures_category" so it's easier to refer
# to the same variable in a function
data_ttest <- data_ttest %>% 
  purrr::map(~ .x %>% rename("measure_category" = 1))

## Before / After comparison for Subgroups -----
# First, define function
ttest_measures <- function(df) {

  df %>%
    mutate(
      # assign months to analysis periods
      period = case_when(
        date == index_baseline ~ "baseline",
        date == index_impact ~ "impact",
        TRUE ~ NA_character_
      ),
      numerator = all_sc_overdue_monitoring_num
    ) %>%
    # remove if date is not in comparison period
    filter(!is.na(period)) %>%
    # aggregate data within periods
    group_by(measure_name, measure_category, period) %>%
    summarise(
      population = sum(population),
      numerator  = sum(numerator),
      value = numerator / population
    ) %>%
    pivot_wider(
      id_cols = c("measure_name", "measure_category"),
      names_from = period,
      values_from = c("population", "numerator", "value")
    ) %>%
    mutate(
      difference = value_impact - value_baseline,
      std.error_baseline = sqrt((value_baseline * (1 - value_baseline)) / population_baseline),
      std.error_impact = sqrt((value_impact * (1 - value_impact)) / population_impact),

      std.error = sqrt((std.error_baseline^2) + (std.error_impact^2)),
      test.stat = difference / std.error,

      p.value = pchisq(test.stat^2, df = 1, lower.tail = FALSE),

      difference.ll = difference + qnorm(0.025) * std.error,
      difference.ul = difference + qnorm(0.975) * std.error
      ) %>%
      ungroup() %>%
      mutate(measure_category = as.character(measure_category))
}

# Apply ttest function to every element in the list and return ONE dataframe
data_ttest_results <- data_ttest %>% 
  purrr::map_dfr(~ .x %>% ttest_measures())

### HETEROGENEITY TESTING FOR SUBGROUPS -----

## Test AGE group-specific differences in baseline/impact difference -----
data_heterogenity_results <- data_ttest_results %>%
  group_by(measure_name) %>%
  summarise(
    # heterogeneity tests
    cochrans_q = sum((1 / (std.error^2)) * ((difference - weighted.mean(difference, 1 / (std.error)^2))^2)),
    p_value = pchisq(cochrans_q, df = n() - 1, lower.tail = FALSE)
  )

# Join results and wirte csv file
data_ttest_results %>%
  left_join(data_heterogenity_results, by = "measure_name") %>%
  mutate(measure_name = str_replace(measure_name, "measure_all_sc_overdue_monitoring_by_", ""),
         measure_name = str_replace(measure_name, "_rate", "")) %>%
  write_csv(here("output/analysis/measures_subgroup_ttest_heterogeneity.csv"))
