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
