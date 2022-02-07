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
