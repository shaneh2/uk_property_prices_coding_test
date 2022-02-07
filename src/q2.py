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
