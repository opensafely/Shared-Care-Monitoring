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


## Before / After comparison for POPULATION -----
data_test <- data_measures$measure_all_sc_overdue_monitoring_rate

data_test %>%
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
    difference.ul = difference + qnorm(0.975)*std.error,

    #Create new dataframe which contains calculated values
    df <- data.frame(value_impact, value_baseline, difference, test.stat, p.value, difference.ll, difference.ul),

    #Output new dataframe with calculated values as a new table
    write.table(df, file="population_t_test.csv", row.names=F, sep=",")
  )



## Before / After comparison for AGE BANDS -----
data_test <- data_measures$measure_all_sc_overdue_monitoring_by_age_band_rate

data_ttest_age_band <-
  data_test %>%
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
  group_by(measure_name, age_band, period) %>%
  summarise(
    population = sum(population),
    numerator  = sum(numerator ),
    value = numerator/population
  ) %>%
  pivot_wider(
    id_cols = c("measure_name", "age_band"),
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
    difference.ul = difference + qnorm(0.975)*std.error,

  )

## Test AGE group-specific differences in baseline/impact difference ----
data_ttest_age_band %>%
  ungroup() %>%
  summarise(
    # heterogeneity tests
    Q = sum((1/(std.error^2) ) * (( difference -weighted.mean(difference, 1/(std.error)^2))^2)),
    p = pchisq(Q, df=n()-1, lower.tail=FALSE),

    #Create new dataframe which contains calculated values
    df_age_chi <- data.frame(Q, p),

    #Output new dataframe with calculated values as a new table
    write.table(df_age_chi, file="age_band_chi_squared.csv", row.names=F, sep=","),

  )