### IMPORT LIBRARIES ----
library('tidyverse')
library('lubridate')
library('here')


### PRELIMINARY SETUP ----

## Define input/output directories ----

# Where the measures files are stored
measures_dir <- here("output", "joined")

# Where to output the results
fs::dir_create(here("output", "analysis"))
analysis_dir <- here("output", "analysis")


## Import measures ----

# Import all measure csv files from input directory
measures_path_all <- fs::dir_ls(path=measures_dir, glob="*.csv", type="file")

# Exclude files with date suffix to only capture summary files
measures_path_summary <- measures_path_all[!str_detect(measures_path_all, "\\_\\d+\\-\\d+\\-\\d+\\.csv$")]

# Capture name of measure from filename
measure_name <-
  measures_path_summary %>%
  fs::path_file() %>%
  fs::path_ext_remove()

# Extract data from measures files and put each dataset in a list
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


## Define dates for time-periods of interest ----
index_baseline <- date("2020-03-01")
index_impact <- date("2020-06-01")


## Prepare dataset for looping through subgroups ----

# Create empty list for dataframes to be used in the loop
data_ttest <- list()

# Create vector with measure names - only including those needed for t-tests
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

# Create 'for loop' that runs only through the measures defined in vector above
for (measure_name in measures_ttest) {
  print(measure_name)
  data_ttest[[measure_name]] <- data_measures[[measure_name]]
}

# Check that the names of the new list only includes the desired measures
names(data_ttest)

# Rename all measure variables as "measures_category" so it's easier to refer to the same variable in a function
data_ttest <- data_ttest %>% 
  purrr::map(~ .x %>% rename("measure_category" = 1))


### T - TEST FOR POPULATION
df_ttest_results_population <- data_measures$measure_all_sc_overdue_monitoring_rate %>%
  # Assign months to analysis time-periods
  mutate(
    period = case_when(
      date == index_baseline ~ "baseline",
      date == index_impact ~ "impact",
      TRUE ~ NA_character_
    ),
    numerator = all_sc_overdue_monitoring_num
  ) %>%
  # Remove if date is not in comparison time-period
  filter(!is.na(period)) %>%
  # Aggregate data within time-periods
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
  #Calculate t-test statistic values
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
# Save results as csv
df_ttest_results_population %>%
  mutate(measure_name = "population") %>%
  write_csv(here("output/analysis/measures_population_ttest.csv"))


### T - TEST FOR SUBGROUPS -----

## Define function for t-test calculation----
ttest_measures <- function(df) {
  df %>%
    mutate(
      # Assign months to analysis time-periods
      period = case_when(
        date == index_baseline ~ "baseline",
        date == index_impact ~ "impact",
        TRUE ~ NA_character_
      ),
      numerator = all_sc_overdue_monitoring_num
    ) %>%
    # Remove if date is not in comparison time-period
    filter(!is.na(period)) %>%
    # Aggregate data within periods
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
    #Calculate t-test statistic values
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

## Apply t-test function to every element in the list and return ONE dataframe ----
data_ttest_results <- data_ttest %>% 
  purrr::map_dfr(~ .x %>% ttest_measures())

#Remove Columns Showing Unredacted Patient Counts
df <- subset[df, select = -c("population_baseline", "population_impact", "numerator_baseline", "numerator_impact")]


### HETEROGENEITY TESTING FOR SUBGROUPS -----

## Test subgroup-specific differences for change in monitoring rate between baseline/impact time-periods -----
data_heterogenity_results <- data_ttest_results %>%
  # Aggregate data within subgroups
  group_by(measure_name) %>%
  # Calculate heterogeneity statistic values
  summarise(
    cochrans_q = sum((1 / (std.error^2)) * ((difference - weighted.mean(difference, 1 / (std.error)^2))^2)),
    p_value = pchisq(cochrans_q, df = n() - 1, lower.tail = FALSE)
  )

## Output Results ----
data_ttest_results %>%
  #Join heterogeneity results with t-test results
  left_join(data_heterogenity_results, by = "measure_name") %>%
  mutate(measure_name = str_replace(measure_name, "measure_all_sc_overdue_monitoring_by_", ""),
         measure_name = str_replace(measure_name, "_rate", "")) %>%
  #Save joined output as csv
  write_csv(here("output/analysis/measures_subgroup_ttest_heterogeneity.csv"))