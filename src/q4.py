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
