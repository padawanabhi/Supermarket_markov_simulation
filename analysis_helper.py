"""_summary_

Returns:
    _type_: _description_
"""
import os
from datetime import time
import pandas as pd

# pylint: disable=C0301

DEFAULT_EXIT_TIME = time(21, 51)


def add_unique_id(dataframe: pd.DataFrame)-> pd.DataFrame:
    """Adds column with a unique identifier for each customer in the dataframe

    Args:
        dataframe (pd.DataFrame): A Dataframe

    Returns:
        pd.DataFrame: A Dataframe
    """
    try:
        dataframe.sort_index(inplace=True)
        dataframe['unique_id'] = (dataframe.customer_no.astype(str) + \
                        '.' + dataframe.index.day_of_week.astype(str)).astype(float)
    except:
        print('The unique id could not be added')
        
    return dataframe


def complete_checkout(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add checkout for customers who have not yet checked out at 21:51 hrs to the DataFrame.

    Args:
        dataframe (pd.DataFrame): Initial dataframe with customer data

    Returns:
        pd.DataFrame: _description_
    """

    checked_out = dataframe[dataframe.location == 'checkout'][['customer_no']]
    date = dataframe.index.date[0]
    timestamp = pd.Timestamp.combine(date=date, time=DEFAULT_EXIT_TIME)
    unchecked = []
    for customer in dataframe.customer_no.unique():
        if customer not in checked_out.customer_no.unique():
            unchecked.append(customer)

    unchecked_df = pd.DataFrame({'timestamp': [timestamp]*len(unchecked), \
                                'customer_no': unchecked, \
                                'location': ['checkout']*len(unchecked)})

    unchecked_df.set_index('timestamp', inplace=True)

    checkout_completed_df = pd.concat([dataframe, unchecked_df], axis=0)
    checkout_completed_df.sort_index(inplace=True)

    return checkout_completed_df


def add_missing_time(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add the missing time steps for each customer to the dataframe.
    Args:
        dataframe (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    new_df = dataframe.groupby('customer_no')[['location']].resample('T').fillna(method="ffill").reindex()
    final_df = new_df.reset_index(level=['customer_no', 'timestamp']).sort_values(['timestamp', 'customer_no']).set_index('timestamp')
    final_df.sort_index(inplace=True)
    return final_df


def combine_data(filepath: str) -> pd.DataFrame:
    """_summary_

    Args:
        filepath (str): Path to the customer data csv files

    Returns:
        pd.DataFrame: DataFrame with data for the whole week.
    """
    df_list = []
    for file in os.listdir(filepath):
        if file.endswith(".csv"):
            data = pd.read_csv(f"./data/{file}", delimiter=";", parse_dates=True, index_col="timestamp")
            data = complete_checkout(dataframe=data)
            data = add_missing_time(dataframe=data)
            data = add_unique_id(dataframe=data)
            df_list.append(data)
    data_combined = pd.concat(df_list, sort=True)
    return data_combined
