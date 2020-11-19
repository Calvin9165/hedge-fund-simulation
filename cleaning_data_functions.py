import pandas as pd




def clean_om_funds_from_dataphile(df):

    cols_to_remove = {

        'Short Name',
        'Price Date',
        'Day',
        'Funds',
        'Market Code',
        'Market',
        'Price Source',
        'Bid Price',
        'Ask Price',
        'Statement Price',
        'Update Date',
        'Trade Volume',
        'Price Status',
        'Statement Price Status',
        'CUSIP'
    }

    # set index
    df['Date'] = pd.to_datetime(df['Price Date'], dayfirst=False)
    df.set_index(keys='Date', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    # rename the price column to whatever security we're using
    df.rename({'Last Trade Price': df['CUSIP'][0]}, axis=1, inplace=True)

    # remove all of the excess columns - we can specify which ones we want to remove
    df.drop(labels=cols_to_remove, axis=1, inplace=True)

    # remove prices with none values (i.e. weekends)
    df.dropna(how='any', axis=0, inplace=True)

    return df


def start_date_finder(dates, how):

    start_date = dates[0]

    if how == 'oldest':

        for date in dates[1:]:
            if date <= start_date:
                start_date = date

    elif how == 'newest':

        for date in dates[1:]:
            if date >= start_date:
                start_date = date

    else:
        return ValueError("Incorrect parameter entry for how parameter, must be 'newest' or 'oldest'")

    return start_date


def end_date_finder(dates, how):
    end_date = dates[0]

    if how == 'oldest':

        for date in dates[1:]:
            if date <= end_date:
                end_date = date

    elif how == 'newest':

        for date in dates[1:]:
            if date >= end_date:
                end_date = date

    else:
        return ValueError("Incorrect parameter entry for how parameter, must be 'newest' or 'oldest'")

    return end_date