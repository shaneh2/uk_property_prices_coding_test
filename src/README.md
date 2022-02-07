# Coding Test Report
This coding test is about using Python Pandas to do some queries about UK property price data.

In this report, I include all the code, and a sample output for each question.

## How to compile:
The command `make` runs the analysis and automatically generates this report:
 * The raw data will be downloaded and saved in feather format using `curl` and `0prepare_data.py` if it hasn't already been.
 * Then the code in `q1.py`,..., `q4.py` will be run.
 * The outputs of the code will be shown in README.md in this directory.

## Requirements
 * I'm using a MacOS 11.2.3 computer, with Xcode command line tools installed (to use `make`).
 * To install the required Python packages, run `make install_required_pip_packages`.
 * If pip isn't installed, try `make install_pip`.

## Loading data from feather file
This data is automatically downloaded: https://www.gov.uk/guidance/about-the-price-paid-data

```python
import pandas as pd
FEATHER_FILE_LOCATION = "../data/full_data_feather.feather"
df = pd.read_feather(FEATHER_FILE_LOCATION)
```



# Q1: Most expensive houses by county
Implement a function that will take price paid data and return another DataFrame containing the full details of the largest transaction occurring within each county present in the data.

___  Property types: D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes, O = Other___

```python
import pandas as pd


def get_most_expensive_houses_by_county(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the most expensive houses in each county, from the inputted pandas DataFrame
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame with highest transaction values in each county
    """
    indices_of_interest = list(df.groupby('County').max("Price")['index'])
    return df.iloc[indices_of_interest]


'''
Here is an example of this function being used:
'''
get_most_expensive_houses_by_county(df)

```

```
         index                                     UID   Price  \
831595  831595  {AE4D86D4-632F-4619-E053-6C04A8C03CD0}  250000
829652  829652  {B82222EC-78B8-6691-E053-6B04A8C02FB2}  240000
796828  796828  {B82222ED-8CF4-6691-E053-6B04A8C02FB2}   65000
773654  773654  {AC07BBD0-B528-0445-E053-6C04A8C01E31}  108000
831726  831726  {AE4D86D4-BA46-4619-E053-6C04A8C03CD0}   50000
...        ...                                     ...     ...
829980  829980  {B82222EC-7F11-6691-E053-6B04A8C02FB2}  460000
813101  813101  {B82222ED-772C-6691-E053-6B04A8C02FB2}  528000
831570  831570  {AE4D86D4-60E6-4619-E053-6C04A8C03CD0}  175000
831453  831453  {AE4D86D4-7CF4-4619-E053-6C04A8C03CD0}  105000
806533  806533  {BEF7EBBF-3034-7A76-E053-6B04A8C092F7}  250000

       Date_of_transfer  Postcode Property_type Old_or_new Duration  \
831595       2020-03-06   BA2 0FE             T          Y        F
829652       2020-10-29  MK43 9BX             S          N        F
796828       2020-11-02   BB2 1AX             T          N        F
773654       2020-05-22   FY5 3JP             S          N        F
831726       2020-06-12  NP13 1EX             T          N        F
...                 ...       ...           ...        ...      ...
829980       2020-10-12  RG41 4BA             D          N        F
813101       2020-10-23   B97 6QH             T          N        F
831570       2020-07-03   TF1 3HW             S          N        F
831453       2020-07-03  LL14 2PW             S          N        F
806533       2020-07-31  YO10 3EB             S          N        F

                       PAON               SAON             Street  \
831595                   12               None    HERBERT GARDENS
829652                   72               None        FOLKES ROAD
796828                   2A               None     SIMMONS STREET
773654                   31               None  LAUDERDALE AVENUE
831726                   21               None        ADAM STREET
...                     ...                ...                ...
829980                   28               None      BLAGROVE LANE
813101            TACK FARM     LONG VIEW BARN        HEWELL LANE
831570                    4               None       ONSLOW DRIVE
831453                    6               None          CEFN PARC
806533  ST. JOSEPHS CONVENT  THE ORCHARD HOUSE    LAWRENCE STREET

           Locality           Town_city                      District
\
831595  FARMBOROUGH                BATH  BATH AND NORTH EAST SOMERSET
829652      WOOTTON             BEDFORD                       BEDFORD
796828         None           BLACKBURN         BLACKBURN WITH DARWEN
773654         None  THORNTON-CLEVELEYS                     BLACKPOOL
831726         None         ABERTILLERY                 BLAENAU GWENT
...             ...                 ...                           ...
829980         None           WOKINGHAM                     WOKINGHAM
813101         None            REDDITCH                    BROMSGROVE
831570   WELLINGTON             TELFORD                        WREKIN
831453      PENYCAE             WREXHAM                       WREXHAM
806533         None                YORK                          YORK

                              County PPD_cat Record_status
831595  BATH AND NORTH EAST SOMERSET       A             A
829652                       BEDFORD       A             A
796828         BLACKBURN WITH DARWEN       A             A
773654                     BLACKPOOL       B             A
831726                 BLAENAU GWENT       B             A
...                              ...     ...           ...
829980                     WOKINGHAM       A             A
813101                WORCESTERSHIRE       A             A
831570                        WREKIN       A             A
831453                       WREXHAM       A             A
806533                          YORK       A             A

[113 rows x 17 columns]
```



# Q2: Top 5 districts by quarterly transaction value
Implement a function that will take price paid data and return a DataFrame (indexed by quarter) giving the 5 postcode districts (i.e. AB1 2CD => AB1) with the largest total transaction value for each quarter (and these values).


```python
import pandas as pd


def get_districts_with_highest_transaction_values_each_quarter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the districts with the highest transaction values in each quarter
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame with, for each quarter, the 5 districts with the highest total transaction values
    """
    # Using this guide to regex: https://stackoverflow.com/a/2013150
    df['District'] = df['Postcode'].str.extract("([^ ]*)")
    quarters_column = pd.DatetimeIndex(df['Date_of_transfer']).quarter.astype(str)
    years_column = pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str)
    df['Quarter'] = 'Q' + quarters_column + ' ' + years_column
    # How to do sorting within nested groupBy: https://stackoverflow.com/a/36074520
    return df.groupby(['Quarter', 'District']) \
        .sum('Price') \
        .sort_values(['Quarter', 'Price'], ascending=False) \
        .groupby('Quarter') \
        .head(5)


'''
Here is an example of this function being used:
'''
get_districts_with_highest_transaction_values_each_quarter(df)

```

```
                      index       Price
Quarter District
Q4 2020 W1S         6090761  1191443381
        E16       103930674   750244361
        SW18      150040876   459780259
        SW1Y        2695312   449288000
        E14       284000973   440253650
Q3 2020 E14       238931589  1931174465
        SE1       110615038   555146127
        SW11      164096367   333914534
        W2         84725234   325618022
        WC1N        5473554   301345000
Q2 2020 W2         63782275   429201234
        EC1V       14238422   392146450
        W1T         6033407   333387572
        SW7        11730800   283387787
        E1         42847887   228751875
Q1 2020 SE1       109221592   356539240
        NW1        57612202   345409923
        SW5        20870688   335527921
        SW11      163066260   327255569
        WC2A       44132146   322397306
```




# Q3: Transaction value concentration
Implement a function that will take price paid data and return a DataFrame, indexed by year and with one column for each property type, giving the percentage of transactions (in descending order of size) that account for 80% of the total transaction value occurring for that property type for each year.


```python
import pandas as pd


def percent_of_transactions_of_each_type_in_top_80pcnt(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the percent of transactions of each type which make up the top 80% of transactions by value
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame broken down by year and property type, which shows the percentage of transactions which sum in
            value to 80% of total transaction value
    """
    #A column contaning the concatenation of the "year" and "type" strings:
    df['YearAndType'] = pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str) + df['Property_type']

    #80% of the transaction total for each year and type:
    transactions_summation_df = _get_transaction_total_for_each_year_and_type(df)
    transactions_summation_df['Price'] = 0.8 * transactions_summation_df['Price']
    transactions_summation_df.rename(columns={'Price': '80% of Total Transaction Value'}, inplace=True)

    #The value of all sales in this year-and-type combination which is greater than this transaction:
    sorted_transactions_df = _value_of_all_sales_in_year_and_type_which_are_greater_than_this_transaction(df)

    #Taking the (sorted) transactions dataframe, and adding extra columns which tell us about the totals for that year and type:
    sorted_with_category_totals_df = pd.merge(sorted_transactions_df, transactions_summation_df,
                                              on='YearAndType')

    #Adding a boolean column which says if that transaction is within the top 80% by value for that year-and-type:
    sorted_with_category_totals_df['in_top_80%_of_value'] = sorted_with_category_totals_df['cumsum'] < \
                                                            sorted_with_category_totals_df[
                                                                '80% of Total Transaction Value']
    query_result = sorted_with_category_totals_df \
        .groupby('YearAndType') \
        .mean('in_top_80%_of_value') \
        .reset_index()[['YearAndType', 'in_top_80%_of_value']]
    query_result['Percent in top 80% of value'] = 100 * query_result['in_top_80%_of_value']
    return query_result


def _value_of_all_sales_in_year_and_type_which_are_greater_than_this_transaction(df: pd.DataFrame)->pd.DataFrame:
    """

    :param df:  a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data,
                but with a YearAndType column
    :return: DataFrame, describing for each transaction, the total value of all transactions of that year and type,
                which are greater in value to this transaction, including this transaction
    """
    sorted_transactions_df = df.sort_values(['YearAndType', 'Price'], ascending=False)
    sorted_transactions_df['cumsum'] = sorted_transactions_df.groupby('YearAndType')['Price'].transform(
        pd.Series.cumsum)
    return sorted_transactions_df


def _get_transaction_total_for_each_year_and_type(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data,
                but with a YearAndType column
    :return: DataFrame, which includes the total value of each transaction type for each year, multiplied by 0.8
    """
    transactions_summation_df = df.groupby(['YearAndType']).sum('Price').reset_index().drop(['index'], axis=1)
    return transactions_summation_df


'''
Here is an example of this function being used:
'''
percent_of_transactions_of_each_type_in_top_80pcnt(df)

```

```
  YearAndType  in_top_80%_of_value  Percent in top 80% of value
0       2020D             0.622919                    62.291940
1       2020F             0.518961                    51.896127
2       2020O             0.132343                    13.234250
3       2020S             0.614201                    61.420057
4       2020T             0.543707                    54.370652
```




# Q4: Volume and median price comparisons

Implement a function that will take two subsets of price paid data and returns a DataFrame showing the percentage change in the number of transactions and their median price between the two datasets, broken down by each of the following price brackets:
  * £0 < x <= 250,000
  * £250,000 < x <= £500,000
  * £500,000 < x <= £750,000
  * £750,000 < x <= £1,000,000
  * £1,000,000 < x <= £2,000,000
  * £2,000,000 < x <= £5,000,000
  * £5,000,000+


```python
from typing import List
import pandas as pd

#We need to specify CUT_BINS, which are the cutoff buckets of property prices. Also, CUT_LABELS is the correspoding strings.
CUT_BINS = [0, 250000, 500000, 750000, 1000000, 2000000, 5000000, float("inf")]
CUT_LABELS = ["£0 < x <= £250,000",
              "£250,000 < x <= £500,000",
              "£500,000 < x <= £750,000",
              "£750,000 < x <= £1,000,000",
              "£1,000,000 < x <= £2,000,000",
              "£2,000,000 < x <= £5,000,000",
              "£5,000,000+"]


def _add_price_buckets_to_df(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a pandas DataFrame, with a new (string) column, indicating which price bucket each transaction is in
    """
    df['Price Bucket'] = pd.cut(df['Price'], bins=CUT_BINS, labels=CUT_LABELS)
    return df


def _get_transaction_count_for_each_price_bucket(df: pd.DataFrame) -> pd.core.series.Series:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data ,
                but with a 'Price Bucket' string column added
    :return: a DataFrame describing the number of transactions in each bucket
    """
    query_result = df.groupby("Price Bucket").size()
    return query_result


def _get_median_price_for_each_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data ,
                but with a 'Price Bucket' string column added
    :return: a DataFrame describing the median transaction value for each price bucket
    """
    query_result = df.groupby("Price Bucket") \
        .median("Price") \
        .reset_index() \
        .drop(['index'], axis=1) \
        .rename(columns={'Price': 'Median Price'})
    return query_result


def __get_percentage_differences_between_two_lists(old_list: List, new_list: List) -> List[float]:
    """
    A utility function for calculating the elementwise percentage differences in values between two lists
    :param old_list: a list of floats/ints
    :param new_list: a list of the same length and types
    :return: a list of percentages, of the same length
    """

    #Note: I decided to implement this function myself, rather than using numpy vector operations, to have more control
    # over special conditions, e.g. if the base number we're comparing to is 0
    percentage_differences_list = []
    assert (len(old_list) == len(new_list))
    for i in range(len(old_list)):
        old = old_list[i]
        new = new_list[i]
        if old == 0:
            difference_percent = 0  # TODO: decide what to do if the number we're comparing with is 0
        else:
            difference_percent = 100 * (new - old) / old
        percentage_differences_list.append(difference_percent)
    return percentage_differences_list


def _get_pcnt_difference_in_transaction_counts(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[float]:
    """
    Gets the percentage difference in transaction counts
    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a list describing the percent differences in transaction counts in each bucket
    """
    old_transation_counts = _get_transaction_count_for_each_price_bucket(last_years_df).values
    new_transaction_counts = _get_transaction_count_for_each_price_bucket(this_years_df).values
    percentage_differences_in_transaction_count = __get_percentage_differences_between_two_lists(old_transation_counts,
                                                                                         new_transaction_counts)
    return percentage_differences_in_transaction_count


def _get_pcnt_difference_in_median_prices_in_buckets(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[
    float]:
    """
    Gets the percent difference in the median transaction price in each bucket
    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a list, describing the percent differences in median transaction value in each bucket
    """
    old_transaction_medians = list(_get_median_price_for_each_bucket(last_years_df)['Median Price'].values)
    new_transaction_medians = list(_get_median_price_for_each_bucket(this_years_df)['Median Price'].values)
    percentage_differences_in_medians = __get_percentage_differences_between_two_lists(old_transaction_medians,
                                                                               new_transaction_medians)
    return percentage_differences_in_medians


def compare_two_dataframes(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> pd.DataFrame:
    """

    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame, which shows the percent differences in total transaction counts and median price paid,
            in each transaction bucket
    """
    last_years_df = _add_price_buckets_to_df(last_years_df.copy())
    this_years_df = _add_price_buckets_to_df(this_years_df.copy())
    percent_differences_in_transaction_counts = _get_pcnt_difference_in_transaction_counts(last_years_df, this_years_df)
    percent_differences_in_median_prices = _get_pcnt_difference_in_median_prices_in_buckets(last_years_df, this_years_df)
    query_result = pd.DataFrame({
        "Price Buckets": CUT_LABELS,
        "Percent difference in number of transactions": percent_differences_in_transaction_counts,
        "Percent difference in median prices": percent_differences_in_median_prices
    }).set_index("Price Buckets")
    return query_result


'''
Here is an example of this function being used, comparing percentage differences between Bath and Bedford:
'''
one_df = df.query("Town_city=='BATH'").copy()
another_df = df.query("Town_city=='BEDFORD'").copy()
compare_two_dataframes(one_df, another_df)

```

```
                              Percent difference in number of
transactions  \
Price Buckets
£0 < x <= £250,000
322.680412
£250,000 < x <= £500,000
158.313539
£500,000 < x <= £750,000
19.157088
£750,000 < x <= £1,000,000
-41.739130
£1,000,000 < x <= £2,000,000
-65.546218
£2,000,000 < x <= £5,000,000
-36.842105
£5,000,000+
80.000000

                              Percent difference in median prices
Price Buckets
£0 < x <= £250,000                                      -2.857143
£250,000 < x <= £500,000                                -3.768116
£500,000 < x <= £750,000                                -1.460122
£750,000 < x <= £1,000,000                              -6.857143
£1,000,000 < x <= £2,000,000                            -2.040816
£2,000,000 < x <= £5,000,000                             9.017857
£5,000,000+                                            178.201220
```


