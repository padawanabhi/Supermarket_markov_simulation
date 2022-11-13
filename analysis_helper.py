import os
import numpy as np
import pandas as pd
from datetime import date, time

DEFAULT_EXIT_TIME = time(21, 51)


def add_unique_id(dataframe)-> pd.DataFrame:

    '''Add unique id for each customer in the dataframe'''

    dataframe.sort_index(inplace=True)
    dataframe['unique_id'] = (dataframe.customer_no.astype(str) + '.' + dataframe.index.day_of_week.astype(str)).astype(float)
    return dataframe


def complete_checkout(dataframe) -> pd.DataFrame:

    '''Add checkout to customers who have not yet checkout out'''

    checked_out = dataframe[dataframe.location == 'checkout'][['customer_no']]
    date = dataframe.index.date[0]
    timestamp = pd.Timestamp.combine(date=date, time=DEFAULT_EXIT_TIME)
    unchecked = []
    for customer in dataframe.customer_no.unique():
        if customer not in checked_out.customer_no.unique():
            unchecked.append(customer)
    
    unchecked_df = pd.DataFrame({'timestamp': [timestamp]*len(unchecked),
                                'customer_no': unchecked, 
                                'location': ['checkout']*len(unchecked)})
    
    unchecked_df.set_index('timestamp', inplace=True)

    checkout_completed_df = pd.concat([dataframe, unchecked_df], axis=0)
    checkout_completed_df.sort_index(inplace=True)

    return checkout_completed_df


def add_missing_time(dataframe) -> pd.DataFrame:

    '''Add missing time for each customer between entering and exiting the store and also add the locaation for that time.'''

    new_df = dataframe.groupby('customer_no')[['location']].resample('T').fillna(method="ffill").reindex()
    final_df = new_df.reset_index(level=['customer_no', 'timestamp']).sort_values(['timestamp', 'customer_no']).set_index('timestamp')
    final_df.sort_index(inplace=True)
    return final_df


def combine_data(filepath):
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

